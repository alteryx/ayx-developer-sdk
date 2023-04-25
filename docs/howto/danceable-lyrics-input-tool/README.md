# Danceable Lyrics
In this guide, we use the [Alteryx Python SDK](https://pypi.org/project/ayx-python-sdk/) and [Alteryx Plugin CLI](https://pypi.org/project/ayx-plugin-cli/) to create tool that connects directly to a set of data files and determines the most "danceable" songs containing a set of lyrics. We will be utilizing [Polars](https://www.pola.rs/) for fast data processing.

# Download Input Data
Download and extract the required dataset files. You will reference them later on in this guide. We provide to sets of this data -- the full and a truncated, smaller version.

* The full version expands to ~11 GiB of data and [can be downloaded here](https://drop.alteryx.com/public/file/SAlShV5VqkOI5_Jyx1me3w/Danceable_Lyrics_demo_data-Inspire-2023.7z).
* A smaller truncated version that expands to ~5.7 GiB of data [can be downloaded here](https://drop.alteryx.com/public/file/yHv77vLzKkCXHj8-OWVg0Q/Danceable_Lyrics_demo_data-Inspire-(Truncated)-2023.7z).

See the `README.md` within the respective archives for source information.

# Basic Plugin Setup
Before proceeding, please ensure you have the following basic setup:

1. [Create a Workspace](create-a-workspace.md) for your plugin to live within.
2. [Add a new plugin](create-a-plugin.md).
    1. When prompted choose **Input** as the type.
    2. To match what is found in this guide, choose **DanceableLyrics** as the plugin name.

After running the above setup procedures, you will see a file named `danceable_lyrics.py` under `./backend/ayx_plugins` with a generated boilerplate. When you open the file, should see something like this:

```python
class DanceableLyrics(PluginV2):
    """Concrete implementation of an AyxPlugin."""

    def __init__(self, provider: AMPProviderV2) -> None:
        self.provider = provider
        # truncated code

    def on_incoming_connection_complete(self, anchor: namedtuple) -> None:
        # truncated code

    def on_record_batch(self, batch: "Table", anchor: namedtuple) -> None:
        # truncated code

    def on_complete(self) -> None:
        import pandas as pd
        import pyarrow as pa

        df = pd.DataFrame(
            {
                "x": [1, 2, 3],
                "y": ["hello", "world", "from ayx_python_sdk!"],
                "z": [self.config_value, self.config_value, self.config_value],
            }
        )

        packet = pa.Table.from_pandas(df)

        self.provider.write_to_anchor("Output", packet)
        self.provider.io.info("DanceableLyrics tool done.")
```

# Write a Plugin!
In this guide, we will be utilzing multiple data files, reading each directly illustrating a "connector" like plugin. That is, to connect directly to local or remote data sources. While we will be reading CSV input files, these could be in any format including those not directly supported by Designer!

> :information_source: To see an Input tool connecting to a remote API, check out [Creating an API Tool](https://github.com/alteryx/ayx-developer-sdk/blob/main/docs/howto/how-to-make-api-tool/api-tool-guide.md)!

> :information_source: Since this is an Input tool, we only focus on the `__init__` and `on_complete` functions. For additional information on the lifecycle of a plugin, refer to the [AYX Python SDK documentation](https://alteryx.github.io/ayx-python-sdk/plugin_lifecycle.html).

## 1. Dependencies
The first thing we'll want to do is update our `./backend/requirements-thirdparty.txt` telling Pything we depend on Polars as a third party depencency. This is as easy as adding a single line to the file:

```txt
polars
```

## 2. Imports
The next step is update our Python module's imports. Imports tell Python what other code we will be referencing in our plugin. Head near the top of your `danceable_lyrics.py` and add the required import statements. Your code should look like this:

```python
from collections import namedtuple

from ayx_python_sdk.core import PluginV2
from ayx_python_sdk.core.field import FieldType
from ayx_python_sdk.core.utils import create_schema
from ayx_python_sdk.providers.amp_provider.amp_provider_v2 import AMPProviderV2

import polars as pl
import pyarrow as pa
```

## 3. Initialization
Let's now update the plugin's `__init__` method, setting up some basic variables we will reference later in the code. To start, modify the start of `__init__` to set a base path to **where your data assets are extracted to** using `self.DATASETS_BASE`. Below is what my copy looks like:

```python
def __init__(self, provider: AMPProviderV2) -> None:
    """Construct a plugin."""
    self.provider = provider
    self.name = "DanceableLyrics"

    self.DATASETS_BASE = "c:/users/bryan.ashby/DanceableLyricsData/"
```

Next, let's tell downstream tools what our plugin's metadata looks like. That is, what fields and their types will we be outputting:

```python
self.provider.push_outgoing_metadata(
    "Output",
    create_schema(
        {
            "artist_name": {"type": FieldType.v_wstring,},
            "track_name": {"type": FieldType.v_wstring,},
            "danceability": {"type": FieldType.float,},
            "energy": {"type": FieldType.float,},
            "track_id": {"type": FieldType.v_wstring,},
        }
    ),
)
```

Great! Now Designer and downstream tooling will know exactly what kind of data to expect from us!

As we would like to find the "most danceable" songs based on particular lyrics, let's provide some terms or phrases. Our tool will gather songs (or "tracks") that contain lyrics with these terms.

```python
self.LYRICS_TERMS = [
    "star wars",
    "star trek",
    "luke skywalker",
    "captain kirk",
    "spock",
    "yoda",
]
```

> :warning: Be aware that these datasets are *not* filtered in any way, and songs or titles may contain explicit content!

Finally, let's add some additional criteria for our analysis and an output message to display when we are initialized. Feel free to play around with these values!

```python
self.DANCEABILITY_RANGE = [0.45, 0.99]
self.ENERGY_RANGE = [0.45, 0.75]
self.TEMPO_RANGE = [110.0, 140.0]
self.MIN_VIEWS = 1000

self.provider.io.info(f"{self.name} initialized.")
```

When you have completed the above steps, your `__init__` should look something like the following:

```python
def __init__(self, provider: AMPProviderV2) -> None:
    """Construct a plugin."""
    self.provider = provider
    self.name = "DanceableLyrics"

    # To build a more flexible plugin, read input path(s) from the user
    self.DATASETS_BASE = "c:/users/bryan.ashby/DanceableLyricsData/"

    self.provider.push_outgoing_metadata(
        "Output",
        create_schema(
            {
                "artist_name": {"type": FieldType.v_wstring,},
                "track_name": {"type": FieldType.v_wstring,},
                "danceability": {"type": FieldType.float,},
                "energy": {"type": FieldType.float,},
                "track_id": {"type": FieldType.v_wstring,},
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
```

> :information_source: To make your Input plugin more dynamic, many of the variables above can be made to be read in from the user using the [Alteryx UI-SDK](https://github.com/alteryx/dev-harness)!

## 4. Data Processing
Now it's time to process some data! Since we do not currently attempt incoming data, but rather, _provide_ data as output, we'll be doing the bulk of our work in `on_complete`.

Our first data input will be from `genius_song_lyrics.csv` in which we will discover songs with lyrics containing our search terms:

```python
def on_complete(self) -> None:
    self.provider.io.info(f"{self.name} gathering sample lyrics...")

    sample = (
        pl.scan_csv(self.DATASETS_BASE + "genius_song_lyrics.csv")
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
```

Above: We are telling Polars to create a `DataFrame` containing select columns from rows matching our criteria. We are also normalizing some column names by lowercasing them and aliasing them in our output. In our `filter` clause, we are building a case-insensitive [Regular Expression](https://en.wikipedia.org/wiki/Regular_expression) from our list of terms. Finally, we filter out non-English terms and restrict to only entries with more than `self.MIN_VIEWS`. You may wish to alter this criteria a bit, for example, by allowing other languages.

The next section of code to build will read from multiple input files and join them into a single `danceable_tracks` view of the data containing columns restricted to our criteria.

```python
self.provider.io.info(f"{self.name} gathering danceable track information...")

artists = (
    pl.scan_csv(self.DATASETS_BASE + "artists.csv")
    .select(
        pl.col("name").str.to_lowercase().alias("artist_name"),
        pl.col("id").alias("artist_id"),
    )
    .collect()
)

tracks = (
    pl.scan_csv(self.DATASETS_BASE + "tracks.csv")
    .select(
        pl.col("name").str.to_lowercase().alias("track_name"),
        pl.col("id").alias("track_id"),
        "explicit",
    )
    .filter(pl.col("explicit") == 0)
    .collect()
)

track_artists = (
    pl.scan_csv(self.DATASETS_BASE + "r_track_artist.csv")
    .select(pl.col("track_id"), pl.col("artist_id"))
    .sort("track_id")
    .collect()
)

audio_features = (
    pl.scan_csv(self.DATASETS_BASE + "audio_features.csv")
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
```

If we were to `print(danceability_tracks)` we'd see a header similar to the following:

```txt
track_id | artist_id | artist_name | track_name | explicit | danceability | energy | tempo
```
As you can see, this is a combination (joined) from multiple sources.


Now that we have both a sample of songs, their lyrics containing our terms, and track information including "danceability", let's find our matches! Add the following code:

```python
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
```

A little explination: The above code loops over all the rows in our sample. By providing `named=True`, Polars will also include the colum name in each `row` value. We then look for a single match (via `limit(1)`) in `danceability_tracks` that have both a matching `artist_name` and `track_name`. Additionally, we build a full Spotify open link by prefixing the `track_id` with a base URL. For any matches, we append to the `matches` `DataFrame`. Finally, we sort the results by `danceability`.

Now that we have our `matches`, let's output them to Designer!

```python
self.provider.write_to_anchor(
    "Output", pa.Table.from_pandas(matches.to_pandas())
)

self.provider.io.info(f"{self.name} finished.")
```

> :information_source: You might notice something a bit odd here: We are constructing a PyArrow table (`pa.Table`) from a Pandas frame converted from Polars. This is due to hhe current version of Polars `to_arrow()` producing somthing not quite right. Perhaps newer versions will no longer require this work around.

## 5. Putting it all Together
Whew, that was a lot! Let's look at what our final `on_complete` should look like:

```python
def on_complete(self) -> None:
    self.provider.io.info(f"{self.name} gathering sample lyrics...")

    sample = (
        pl.scan_csv(self.DATASETS_BASE + "genius_song_lyrics.csv")
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
        pl.scan_csv(self.DATASETS_BASE + "artists.csv")
        .select(
            pl.col("name").str.to_lowercase().alias("artist_name"),
            pl.col("id").alias("artist_id"),
        )
        .collect()
    )

    tracks = (
        pl.scan_csv(self.DATASETS_BASE + "tracks.csv")
        .select(
            pl.col("name").str.to_lowercase().alias("track_name"),
            pl.col("id").alias("track_id"),
            "explicit",
        )
        .filter(pl.col("explicit") == 0)
        .collect()
    )

    track_artists = (
        pl.scan_csv(self.DATASETS_BASE + "r_track_artist.csv")
        .select(pl.col("track_id"), pl.col("artist_id"))
        .sort("track_id")
        .collect()
    )

    audio_features = (
        pl.scan_csv(self.DATASETS_BASE + "audio_features.csv")
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
```

# Package Into a YXI
Now that we've created our code, it's time to package it all up into a portable YXI archive. For this, we will be using the `ayx_plugin_cli create-yxi` command. The process looks like the following:

```bash
~/MyWorkspace$ ayx_plugin_cli create-yxi
[Creating YXI] started
[Creating YXI] -- generate_config_files:generate_config_xml
[Creating YXI] -- generate_config_files:generate_tool_config_xml
[Creating YXI] .  generate_config_files:generate_manifest_jsons
[Creating YXI] Generating manifest.json for DanceableLyrics...
[Creating YXI] Done!
...omitted...
~\MyWorkspace\main.pyz -e ayx_python_sdk.providers.amp_provider.__main__:main
[Creating YXI] Created shiv artifact at: ~\MyWorkspace\main.pyz
[Creating YXI] .  create_yxi:create_yxi
[Creating YXI] finished
```

# Run the Test Client
Before proceeding on to running within Designer, it's good practice to do some basic testing with `ayx-sdk-cli`'s `plugin run` command to check for any errors. From your workspace:

```bash
ayx-sdk-cli plugin run DanceableLyrics -o danceable.csv
```

The above command will run our plugin and produce `danceable.csv`. You may run `ayx-sdk-cli plugin run --help` for additional options.

Given the command above, our output should look something like this (I am using [Rich CLI](https://github.com/Textualize/rich-cli) to preview):

![danceable.csv](danceable-csv.png)

# Install and Run in Designer
In this section we will go over the two ways to install the plugin into Designer.

## Method 1
After you create a .yxi, you can double-click the .yxi to install it into Designer. This opens Designer and prompts you to install the package in a new dialog box. It looks something like this:

![Designer Install Prompt](designer-install-prompt.png)

Once it installs, you can find the plugin under the `Python SDK Examples` tool tab.[^2]

## Method 2
You can also create the `.yxi` _**and**_ install it all at once via the `ayx_plugin_cli designer-install` command. Choose the install option that matches your Designer install. Typically, this is the `user` install option.

```bash
~/MyWorkspace$ ayx_plugin_cli designer-install
Install Type (user, admin) [user]: user
[Creating YXI] started
[Creating YXI] -- generate_config_files:generate_config_xml
[Creating YXI] -- generate_config_files:generate_tool_config_xml
[Creating YXI] .  generate_config_files:generate_manifest_jsons
[Creating YXI] Generating manifest.json for DanceableLyrics...
[Creating YXI] Done!
...omitted...
[Creating YXI] finished
[Installing yxi ~\MyWorkspace\build\yxi\DanceableLyrics.yxi into designer] started
[Installing yxi ~\MyWorkspace\build\yxi\DanceableLyrics.yxi into designer] .  install_yxi
[Installing yxi ~\MyWorkspace\build\yxi\DanceableLyrics.yxi into designer] finished
If this is your first time installing these tools, or you have made modifications to your ayx_workspace.json file, please restart Designer for these changes to take effect. # <-- Done installing into Designer!
```

Once the command finishes you can open Designer and find your tool under the `Python SDK Examples` tab.[^1]

# Run in Designer
When you run this tool in Designer it yields the following output:

![Designer Output](designer-output.png)

You can see that our top danceable track with the input lyrics provided is ["Track 10" by The Procussions](https://open.spotify.com/track/1xZJKDCFXuCRUr82qzaRDp)!

https://open.spotify.com/track/1xZJKDCFXuCRUr82qzaRDp

Thanks for reading, I hope you enjoyed this tutorial!


> [^1]: :warning: If you created the plugin workspace with a non-default `Tool Category` (from the [Create a Workspace](#1-create-a-workspace) section), then the plugin will show up in the tab that corresponds to the input that was passed to `Tool Category`.