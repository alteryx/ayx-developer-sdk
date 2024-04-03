# Copyright (C) 2022 Alteryx, Inc. All rights reserved.
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
"""Example Input Tool"""
from collections import namedtuple

from ayx_python_sdk.core import PluginV2
from ayx_python_sdk.providers.amp_provider.amp_provider_v2 import AMPProviderV2

from pyarrow import Table


class ConstantsExample(PluginV2):
    """Concrete Implementation of an AyxPlugin"""

    def __init__(self, provider: AMPProviderV2) -> None:
        """Construct a plugin."""
        self.provider = provider
        self.config_value = 0.42
        self.provider.io.info("Plugin initialized.")

    def on_incoming_connection_complete(self, anchor: namedtuple) -> None:
        """
        Call when an incoming connection is done sending data including when no data is sent on an optional input anchor.

        This method is not called during update-only mode.

        Parameters
        ----------
        anchor
            NamedTuple contains anchor.name and anchor.connection.
        """
        raise NotImplementedError("Input tools don't receive incoming connections.")

    def on_record_batch(self, batch: "Table", anchor: namedtuple) -> None:
        """
        Process the passed record batch that comes in on the specified anchor.

        The method that gets called whenever the plugin receives a record batch on an input.

        This method is not called during update-only mode.

        Parameters
        ----------
        batch
            A pyarrow Table that contains the received batch.
        anchor
            A namedtuple('Anchor', ['name', 'connection_name']) that contains input connection identifiers.
        """
        raise NotImplementedError("Input tools don't receive batches.")

    def on_complete(self) -> None:
        """
        Clean up any plugin resources, or push records for an input tool.

        This method gets called when all other plugin processing is complete.

        In this method, you should perform any cleanup for your plugin.
        However, if the plugin is an input-type tool (it has no incoming connections),
        processing (record generation) should occur here.

        Note: A tool with an optional input anchor and no incoming connections should
        also write any records to output anchors here.
        """
        import pandas as pd
        import pyarrow as pa

        self.provider.io.info("Raw constants: ")

        for k, v in self.provider.environment.raw_constants.items():
            self.provider.io.info(f"{k}: {v}")

        df = pd.DataFrame(
            {
                "Designer Version": [self.provider.environment.designer_version],
                "Alteryx Install Directory": [str(self.provider.environment.alteryx_install_dir)],
                "Workflow Directory": [str(self.provider.environment.workflow_dir)],
                "Workflow ID": [self.provider.environment.workflow_id],
                "Temp Directory": [str(self.provider.environment.temp_dir)],
                "Tool ID": [self.provider.environment.tool_id],
            }
        )

        packet = pa.Table.from_pandas(df)

        self.provider.write_to_anchor("Output", packet)