# Danceable Lyrics
In this guide, we use the [Alteryx Python SDK](https://pypi.org/project/ayx-python-sdk/) and [Alteryx Plugin CLI](https://pypi.org/project/ayx-plugin-cli/) to create a tool that connects directly to a set of data files and determines the most "danceable" songs that contain a set of lyrics. We use [Polars](https://www.pola.rs/) for fast data processing.

## Table of Contents
* [Download Input Data](#download-input-data)
* [Basic Plugin Setup](#basic-plugin-setup)
* [Write a Plugin](#write-a-plugin)
    * [Dependencies](#1-dependencies)
    * [Imports](#2-imports)
    * [Initialization](#3-initialization)
    * [Data Processing](#4-data-processing)
    * [Putting It All Together](#5-putting-it-all-together)
* [Packaging into a YXI](#package-into-a-yxi)
* [Run the Test Client](#run-the-test-client)
* [Install in Designer](#install-and-run-in-designer)
    * [Method 1](#method-1)
    * [Method 2](#method-2)
* [Run in Designer](#run-in-designer)

## Download Input Data
Download and extract the required dataset files. You will reference them later in this guide. We provide 2 datasets—the full dataset and a smaller, truncated version.

* The full version expands to around 11 GB of data. You can [download it here](https://drop.alteryx.com/public/file/SAlShV5VqkOI5_Jyx1me3w/Danceable_Lyrics_demo_data-Inspire-2023.7z).
* The truncated version expands to around 5.7 GB of data. You can [download it here](https://drop.alteryx.com/public/file/yHv77vLzKkCXHj8-OWVg0Q/Danceable_Lyrics_demo_data-Inspire-(Truncated)-2023.7z).

Go to the `README.md` files within the respective archives for source information.

## Basic Plugin Setup
Before you proceed, please ensure you have this basic setup:

1. [Create a Workspace](create-a-workspace.md) to house your plugin.
2. [Add a new plugin](create-a-plugin.md).
    1. When prompted choose **Input** as the type.
    2. To match what is found in this guide, choose **DanceableLyrics** as the plugin name.

After you run the above setup procedures, you will have a file named `danceable_lyrics.py` under `./backend/ayx_plugins` with a generated boilerplate. When you open the file, you should see something like this:

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

## Write a Plugin
In this guide, we use multiple data files. We read each directly to illustrate a connector-like plugin. That is, to connect directly to local or remote data sources. While here, we read CSV input files, these could be in any format, including formats that Alteryx Designer does not directly support.

> :information_source: To see an Input tool that connects to a remote API, check out [Creating an API Tool](https://github.com/alteryx/ayx-developer-sdk/blob/main/docs/howto/how-to-make-api-tool/api-tool-guide.md)!

> :information_source: Since this is an Input tool, we only focus on the `__init__` and `on_complete` functions. For additional information on the lifecycle of a plugin, refer to the [AYX Python SDK documentation](https://alteryx.github.io/ayx-python-sdk/plugin_lifecycle.html).

### 1. Dependencies
The first step is to update our `./backend/requirements-thirdparty.txt` file and tell Python we depend on Polars as a 3rd-party dependency. To do this, add a single line to the file:

```txt
polars==0.17.9
```

### 2. Imports
The next step is to update our Python module's imports. Imports tell Python what other code we will reference in our plugin. Add the required import statements near the top of your `danceable_lyrics.py` file. Your code should look like this:

```python
from collections import namedtuple

from ayx_python_sdk.core import PluginV2
from ayx_python_sdk.core.field import FieldType
from ayx_python_sdk.core.utils import create_schema
from ayx_python_sdk.providers.amp_provider.amp_provider_v2 import AMPProviderV2

import polars as pl
import pyarrow as pa
```

### 3. Initialization
Now, let's update the plugin's `__init__` method and set up some basic variables that we will reference later in the code. To start, modify the start of `__init__` to set a base path to _where you extracted your data assets_. Use `self.DATASETS_BASE` to do so. The result should look something like this:

```python
def __init__(self, provider: AMPProviderV2) -> None:
    """Construct a plugin."""
    self.provider = provider
    self.name = "DanceableLyrics"

    # Point this variable to your extracted datasets directory:
    self.DATASETS_BASE = "c:/users/alteryx/DanceableLyricsData/"
```

Next, let's tell downstream tools what our plugin's metadata looks like. That is, what fields and their data types the plugin will output:

```python
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
```

Now Designer and downstream tools will know exactly what kind of data to expect from our plugin.

Since we want to find the "most danceable" songs based on particular lyrics, let's provide some terms or phrases. Our tool will then gather songs (or "tracks") that contain lyrics with these terms.

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

> :warning: Be aware that these datasets are *not* filtered in any way, and songs or titles might contain explicit content!

Finally, let's add some additional criteria for our analysis and an output message to display when the plugin is initialized. Feel free to play around with these values!

```python
self.DANCEABILITY_RANGE = [0.45, 0.99]
self.ENERGY_RANGE = [0.45, 0.75]
self.TEMPO_RANGE = [110.0, 140.0]
self.MIN_VIEWS = 1000

self.provider.io.info(f"{self.name} initialized.")
```

When you have completed the above steps, your `__init__` should look something like this:

```python
def __init__(self, provider: AMPProviderV2) -> None:
    """Construct a plugin."""
    self.provider = provider
    self.name = "DanceableLyrics"

    # To build a more flexible plugin, read input path(s) from the user
    self.DATASETS_BASE = "c:/users/alteryx/DanceableLyricsData/"

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

> :information_source: To make your Input plugin more dynamic, you can use the [Alteryx UI-SDK](https://github.com/alteryx/dev-harness) and have a user supply many of the variables above.

### 4. Data Processing
Now it's time to process some data! Since we don't currently attempt incoming data, but rather, _provide_ data as output, we'll do the bulk of our work in `on_complete`.

Our first data input is from the `genius_song_lyrics.csv` file, where we will discover songs with lyrics that contain our search terms:

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

Above, we tell Polars to create a `DataFrame` that contains select columns from rows that match our criteria. We also normalize some column names— we lowercase them and add aliases in our output. In our `filter` clause, we build a case-insensitive [regular expression](https://en.wikipedia.org/wiki/Regular_expression) from our list of terms. Finally, we filter out non-English terms and restrict results to only entries with more than `self.MIN_VIEWS`. You might want to alter these criteria a bit. For example, you might want to allow other languages.

The next section of code reads from multiple input files and joins them into a single `danceable_tracks` view of the data that contains columns that match our criteria.

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
    .collect()
)

audio_features = (
    pl.scan_csv(self.DATASETS_BASE + "audio_features.csv")
    .select(pl.col("id").alias("track_id"), "danceability", "energy", "tempo",)
    .filter(pl.col("danceability").is_between(*self.DANCEABILITY_RANGE))
    .filter(pl.col("energy").is_between(*self.ENERGY_RANGE))
    .filter(pl.col("tempo").is_between(*self.TEMPO_RANGE))
    .collect()
)

danceability_tracks = (
    track_artists.join(artists, on="artist_id")
    .join(tracks, on="track_id")
    .join(audio_features, on="track_id")
)
```

If we output danceability_tracks via `print(danceability_tracks)`, we'll see a header similar to this:

```txt
track_id | artist_id | artist_name | track_name | explicit | danceability | energy | tempo
```
As you can see, this combines data from multiple sources.

Now that we have both a sample of songs with lyrics that contain our terms and track information that includes "danceability", let's find our matches! Add this code:

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

The above code loops over all the rows in our sample. Since we provide `named=True`, Polars also includes the column name in each `row` value. We then look for a single match with a matching `artist_name` and `track_name` (via `limit(1)`) in `danceability_tracks`. Additionally, we prefix the `track_id` with a base URL to build a full Spotify open link. We append to the `matches` `DataFrame` for any matches. Finally, we sort the results by `danceability`.

Now that we have our `matches`, let's output them to Designer!

```python
self.provider.write_to_anchor(
    "Output", pa.Table.from_pandas(matches.to_pandas())
)

self.provider.io.info(f"{self.name} finished.")
```

> :information_source: You might notice something a bit odd here. We are constructing a PyArrow table (`pa.Table`) from a Pandas frame converted from Polars. This is because the current version of Polars `to_arrow()` produces unexpected results. Perhaps newer versions won't require this workaround.

### 5. Putting It All Together
> :information_source: See [danceable_lyrics.py](../danceable-lyrics-input-tool/DanceableLyrics/backend/ayx_plugins/danceable_lyrics.py) for the full source.

Let's take a look at our final `on_complete`. It should look like something like this:

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
        .collect()
    )

    audio_features = (
        pl.scan_csv(self.DATASETS_BASE + "audio_features.csv")
        .select(pl.col("id").alias("track_id"), "danceability", "energy", "tempo",)
        .filter(pl.col("danceability").is_between(*self.DANCEABILITY_RANGE))
        .filter(pl.col("energy").is_between(*self.ENERGY_RANGE))
        .filter(pl.col("tempo").is_between(*self.TEMPO_RANGE))
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

## Package into a YXI
Now that we have our code, it's time to package it all up into a portable YXI archive. To do this, we use the `ayx_plugin_cli create-yxi` command. The process looks like this:

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

## Run the Test Client
Before you run your plugin in Designer, it's good practice to do some basic testing with `ayx-sdk-cli`'s `plugin run` command to check for any errors. From your workspace...

```bash
ayx-sdk-cli plugin run DanceableLyrics -o danceable.csv
```

The above command runs our plugin and produces `danceable.csv`. You can run `ayx-sdk-cli plugin run --help` for additional options.

Given the command above, our output should look something like this (we use [Rich CLI](https://github.com/Textualize/rich-cli) to preview):

![danceable.csv](./assets/danceable-csv.png)

## Install in Designer
In this section, we will go over the 2 ways to install the plugin into Designer.

### Method 1
After you create a .yxi, you can double-click the .yxi to install it in Designer. This opens Designer and prompts you to install the package in a new dialog box. It looks something like this:

![Designer Install Prompt](./assets/designer-install-prompt.png)

Once it installs, you can find the plugin under the `Python SDK Examples` tool category.[^2]

### Method 2
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

Once the command finishes, you can open Designer and find your tool under the `Python SDK Examples` tool category.[^1]

## Run in Designer
When you run this tool in Designer, it produces this output:

![Designer Output](./assets/designer-output.png)

You can see that our top danceable track with the input lyrics provided is ["Track 10" by The Procussions](https://open.spotify.com/track/1xZJKDCFXuCRUr82qzaRDp)!


> [^1]: :warning: If you created the plugin workspace with a non-default `Tool Category` (from the [Create a Workspace](#1-create-a-workspace) section), then your plugin will appear in the tool category that corresponds to the input that you passed to `Tool Category`.