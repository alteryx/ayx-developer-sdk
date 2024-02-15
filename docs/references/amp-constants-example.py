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
"""Example input tool."""
from collections import namedtuple

from ayx_python_sdk.core import PluginV2
from ayx_python_sdk.providers.amp_provider.amp_provider_v2 import AMPProviderV2

from pyarrow import Table


class ConstantsTestTool(PluginV2):
    """Concrete implementation of an AyxPlugin."""

    def __init__(self, provider: AMPProviderV2) -> None:
        """Construct a plugin."""
        self.provider = provider

    def on_incoming_connection_complete(self, anchor: namedtuple) -> None:
        """
        Call when an incoming connection is done sending data including when no data is sent on an optional input anchor.

        This method IS NOT called during update-only mode.

        Parameters
        ----------
        anchor
            NamedTuple containing anchor.name and anchor.connection.
        """
        raise NotImplementedError("Input tools don't receive batches.")

    def on_record_batch(self, batch: "Table", anchor: namedtuple) -> None:
        """
        Process the passed record batch that comes in on the specified anchor.

        The method that gets called whenever the plugin receives a record batch on an input.

        This method IS NOT called during update-only mode.

        Parameters
        ----------
        batch
            A pyarrow Table containing the received batch.
        anchor
            A namedtuple('Anchor', ['name', 'connection_name']) containing input connection identifiers.
        """
        raise NotImplementedError("Input tools don't receive batches.")

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
        import pyarrow as pa

        constants_to_test = ["Engine.WorkflowFileName", "Engine.Type"]
        table = pa.Table.from_arrays(
            list(zip(*[[k, v] for k, v in sorted(
                self.provider.environment.raw_constants.items(), key=lambda k: k
            ) if k in constants_to_test])), names=["key", "value"]
        )
        self.provider.write_to_anchor("Output", table)