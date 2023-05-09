# Copyright (C) 2023 Alteryx, Inc. All rights reserved.
#
# Licensed under the ALTERYX SDK AND API LICENSE AGREEMENT;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.alteryx.com/alteryx-sdk-and-api-license-agreement
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Example input tool."""
from collections import namedtuple

from pathlib import Path

from ayx_python_sdk.core import PluginV2
from ayx_python_sdk.core.exceptions import WorkflowRuntimeError
from ayx_python_sdk.core.field import FieldType
from ayx_python_sdk.core.utils import create_schema
from ayx_python_sdk.providers.amp_provider.amp_provider_v2 import AMPProviderV2

import polars as pl
import pyarrow as pa


class DanceableLyrics(PluginV2):
    """Concrete implementation of an AyxPlugin."""

    @staticmethod
    def _validate_datasets_dir(datasets_dir: Path) -> None:
        if not datasets_dir.is_dir():
            raise WorkflowRuntimeError("Bad path")

        filenames = [
            "artists.csv",
            "tracks.csv",
            "r_track_artist.csv",
            "genius_song_lyrics.csv",
            "audio_features.csv"
        ]
        nonexistent_files = list(
            filter(lambda filepath: not filepath.is_file(), map(lambda filename: (datasets_dir / filename), filenames))
        )

        if len(nonexistent_files) != 0:
            raise WorkflowRuntimeError(
                f"Expected files not found: {','.join(map(str, nonexistent_files))}")

    def __init__(self, provider: AMPProviderV2) -> None:
        """Construct a plugin."""
        self.provider = provider
        self.name = "DanceableLyrics"

        # Point this variable to your extracted datasets directory:
        self.DATASETS_BASE = Path("c:/users/alteryx/DanceableLyricsData/")

        self._validate_datasets_dir(self.DATASETS_BASE)

        self.provider.push_outgoing_metadata(
            "Output",
            create_schema(
                {
                    "artist_name": {"type": FieldType.v_wstring},
                    "track_name": {"type": FieldType.v_wstring},
                    "danceability": {"type": FieldType.float},
                    "energy": {"type": FieldType.float},
                    "track_id": {"type": FieldType.v_wstring},
                }
            ),
        )

        self.LYRICS_TERMS = [
            "star wars",
            "star trek",
            "luke skywalker",
            "captain kirk",
            "spock",
            "yoda",
        ]
        self.DANCEABILITY_RANGE = [0.45, 0.99]
        self.ENERGY_RANGE = [0.45, 0.75]
        self.TEMPO_RANGE = [110.0, 140.0]
        self.MIN_VIEWS = 1000

        self.provider.io.info(f"{self.name} initialized.")

    def on_incoming_connection_complete(self, anchor: namedtuple) -> None:
        raise NotImplementedError("Input tools don't receive batches.")

    def on_record_batch(self, batch: "pa.Table", anchor: namedtuple) -> None:
        raise NotImplementedError("Input tools don't receive batches.")

    def on_complete(self) -> None:
        self.provider.io.info(f"{self.name} gathering sample lyrics...")

        sample = (
            pl.scan_csv(self.DATASETS_BASE / "genius_song_lyrics.csv")
            .select(
                pl.col("title").str.to_lowercase().alias("track_name"),
                pl.col("artist").str.to_lowercase().alias("artist_name"),
                "lyrics",
                "language",
                "views",
            )
            .filter(
                pl.col("lyrics").str.contains("(?i)" + "|(?i)".join(self.LYRICS_TERMS))
            )
            .filter(pl.col("language") == "en")
            .filter(pl.col("views") > self.MIN_VIEWS)
            .collect()
        )

        self.provider.io.info(f"{self.name} gathering danceable track information...")

        artists = (
            pl.scan_csv(self.DATASETS_BASE / "artists.csv")
            .select(
                pl.col("name").str.to_lowercase().alias("artist_name"),
                pl.col("id").alias("artist_id"),
            )
            .collect()
        )

        tracks = (
            pl.scan_csv(self.DATASETS_BASE / "tracks.csv")
            .select(
                pl.col("name").str.to_lowercase().alias("track_name"),
                pl.col("id").alias("track_id"),
                "explicit",
            )
            .filter(pl.col("explicit") == 0)
            .collect()
        )

        track_artists = (
            pl.scan_csv(self.DATASETS_BASE / "r_track_artist.csv")
            .select(pl.col("track_id"), pl.col("artist_id"))
            .sort("track_id")
            .collect()
        )

        audio_features = (
            pl.scan_csv(self.DATASETS_BASE / "audio_features.csv")
            .select(pl.col("id").alias("track_id"), "danceability", "energy", "tempo",)
            .filter(pl.col("danceability").is_between(*self.DANCEABILITY_RANGE))
            .filter(pl.col("energy").is_between(*self.ENERGY_RANGE))
            .filter(pl.col("tempo").is_between(*self.TEMPO_RANGE))
            .sort("track_id")
            .collect()
        )

        danceability_tracks = (
            track_artists.join(artists, on="artist_id")
            .join(tracks, on="track_id")
            .join(audio_features, on="track_id")
        )

        self.provider.io.info(f"{self.name} calculating final results...")

        matches = pl.DataFrame()
        for row in sample.rows(named=True):
            artist = row["artist_name"]
            track = row["track_name"]
            m = (
                danceability_tracks.select(
                    "artist_name",
                    "track_name",
                    "danceability",
                    "energy",
                    ("https://open.spotify.com/track/" + pl.col("track_id")),
                )
                .filter(pl.col("artist_name") == artist)
                .filter(pl.col("track_name") == track)
                .limit(1)
            )

            if not m.is_empty():
                matches = pl.concat([matches, m])

        matches = matches.sort("danceability", descending=True)

        self.provider.write_to_anchor(
            "Output", pa.Table.from_pandas(matches.to_pandas())
        )

        self.provider.io.info(f"{self.name} finished.")