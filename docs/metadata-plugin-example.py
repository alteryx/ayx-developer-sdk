"""Example metadata tool."""
from typing import TYPE_CHECKING
 
from ayx_python_sdk.core import (
    Anchor,
    PluginV2,
)
from ayx_python_sdk.core.utils import *
from ayx_python_sdk.providers.amp_provider.amp_provider_v2 import AMPProviderV2
from ayx_python_sdk.core.field import FieldType as FT
 
if TYPE_CHECKING:
    import pyarrow as pa
 
import pandas as pd
 
 
class Metadata(PluginV2):
    """A sample Plugin that passes data from an input connection to an output connection."""
 
    def __init__(self, provider: AMPProviderV2):
        """Construct the plugin."""
        self.name = "metadata"
        self.provider = provider
        self.outputschema = create_schema({
                "volts":{
                "type":FT.int16,
                "size":2,
                "source":"Nuclear power",
                "description":"Uranium and plutonium"}, 
                "year":{
                "type":FT.string,
                "size":4,
                "source":"Year of work",
                "description":"For all people in the world"}, 
                "bool":FT.bool,
                "byte":FT.byte,
                "int16":FT.int16,
                "int32":FT.int32,
                "int64":FT.int64,
                "fixeddecimal":{"type":FT.fixeddecimal,"size":128,"scale":120},
                "float":FT.float,
                "double":FT.double,
                "string":FT.string,
                "wstring":FT.wstring,
                "v_string":FT.v_string,
                "v_wstring":FT.v_wstring,
                "date":FT.date,
                "time":FT.time,
                "datetime":FT.datetime,
                "spatialobj":FT.spatialobj})
        provider.push_outgoing_metadata("Output", self.outputschema)
 
        self.provider.io.info(f"{self.name} tool started")
 
    def on_record_batch(self, batch: "pa.Table", anchor: Anchor) -> None:
        """
        Process the passed record batch.
 
        The method that gets called whenever the plugin receives a record batch on an input.
 
        This method IS NOT called during update-only mode.
 
        Parameters
        ----------
        batch
            A pyarrow Table containing the received batch.
        anchor
            A namedtuple('Anchor', ['name', 'connection']) containing input connection identifiers.
        """
 
        df = pd.DataFrame(
            {
                "volts": [1,32000,32100],
                "year":["2022","202235", "testtest"],
                "bool":[True,False,True],
                "byte":[1, 124, 255],
                "int16":[1, 32000, 32767],
                "int32":[1, 1001, 2147483647],
                "int64":[1, 9223372036854775807, 9223372036854775804],
                "fixeddecimal":[4544544.4515112, 11110.77777, 78445.1102],
                "float":[4544544.4515112, 11110.77777, 7844512.1102124],
                "double":[4544544.4515112, 11110.77777, 7844512.1102124],
                "string":["this is", "a simple", "string"],
                "wstring":["this is", "a simple", "string"],
                "v_string":["this is", "a simple", "string"],
                "v_wstring":["this is", "a simple", "string"],
                "date":[to_date("08/10/2022"), to_date("08/22/2022"), to_date("08/01/1987")],
                "time":[to_time("08:45:26"),to_time("15:55:10"),to_time("18:10:10")],
                "datetime":[to_datetime("08/22/2022 00:00:00"),to_datetime("08/22/2022 00:00:00"),to_datetime("08/22/2022 00:00:00")],
                "spatialobj":["POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))",
                    "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))",
                    "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))"]
            }
        )
 
        batch = pa.Table.from_pandas(df)
        batch = set_metadata(batch, schema=self.outputschema)
        all_metadata = get_metadata(batch)
        self.provider.io.info(str(all_metadata))
 
        self.provider.write_to_anchor("Output", batch)
 
    def on_incoming_connection_complete(self, anchor: Anchor) -> None:
        """
        Call when an incoming connection is done sending data including when no data is sent on an optional input anchor.
 
        This method IS NOT called during update-only mode.
 
        Parameters
        ----------
        anchor
            NamedTuple containing anchor.name and anchor.connection.
        """
        self.provider.io.info(
            f"Received complete update from {anchor.name}:{anchor.connection}."
        )
 
    def on_complete(self) -> None:
        """
        Clean up any plugin resources, or push records for an input tool.
 
        This method gets called when all other plugin processing is complete.
 
        In this method, a Plugin designer should perform any cleanup for their plugin.
        However, if the plugin is an input-type tool (it has no incoming connections),
        processing (record generation) should occur here.
 
        Note: A tool with an optional input anchor and no incoming connections should
        also write any records to output anchors here.
        """
        self.provider.io.info(f"{self.name} tool done.")
```
