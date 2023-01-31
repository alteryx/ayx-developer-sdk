# Creating a tool with an API hit
In this guide, we will use the [Alteryx Python SDK](https://pypi.org/project/ayx-python-sdk/) and [Alteryx Plugin CLI](https://pypi.org/project/ayx-plugin-cli/) to create a tool that pulls information from an API and find the mean, min, and max of the data.

## Creating a workspace
The very first step to creating a plugin is to make a plugin workspace. We initialize a plugin workspace in an empty directory with the `sdk-workspace-init` command. Run the command and fill out the prompts, which will then start the workspace initialization process.

```
$ ayx_plugin_cli sdk-workspace-init
Package Name: API Tool
Tool Category [Python SDK Examples]: 
Description []: API Tool
Author []: Alteryx
Company []: Alteryx
Backend Language (python): python
[Workspace initialization] started
[Workspace initialization] .  Create configuration directory
[Workspace initialization] .  Create DCM Schemas directory
[Workspace initialization] .  Create .gitignore
[Workspace initialization] .  Create README.md
[Workspace initialization] .  Initialize backend
[Workspace initialization] Creating ~\sdk-api-tool\backend\ayx_plugins
[Workspace initialization] Creating file ~\sdk-api-tool\backend\requirements-local.txt
[Workspace initialization] Creating file ~\sdk-api-tool\backend\requirements-thirdparty.txt
[Workspace initialization] Creating file ~\sdk-api-tool\backend\setup.py
[Workspace initialization] Creating file ~\sdk-api-tool\backend\ayx_plugins\__init__.py
[Workspace initialization] .  Create tests directory
[Workspace initialization] .  Initialize UI
[Workspace initialization] finished
Created Alteryx workspace in directory: ~\sdk-api-tool
Workspace settings can be modified in: ayx_workspace.json
[Generating config files] started
[Generating config files] .  generate_config_files:generate_config_xml
[Generating config files] Generating top level config XML file...
[Generating config files] finished
```

## Creating a plugin
The next step is to add a plugin to the workspace. We do this using the `create-ayx-plugin` command. Fill out the prompts and then you will have the template code for your SDK Plugin. For this tool, we are choosing the `Input` tool type.

```
$ ayx_plugin_cli create-ayx-plugin
Tool Name: API tool
Tool Type (input, multiple-inputs, multiple-outputs, optional, output, single-input-single-output, multi-connection-input-anchor) [single-input-single-output]: input
Description []: My API Tool
Tool Version [1.0]: 1.0
DCM Namespace []:
Creating input plugin: API tool
[Create plugin] started
[Create plugin] Downloading UI components via git
[Create plugin] Cloning into '.ayx_cli.cache\ui_tool_template'...
[Create plugin] .  Create plugin
[Create plugin] Installing UI components via npm
[Create plugin] Creating Alteryx Plugin...
[Create plugin] Copying example tool to ~\sdk-api-tool\backend\ayx_plugins...
[Create plugin] Added new tool to package directory: ~\sdk-api-tool\backend\ayx_plugins\a_p_i_tool.py
[Create plugin] finished
[Generating config files] started
[Generating config files] .  generate_config_files:generate_config_xml
[Generating config files] Generating top level config XML file...
[Generating config files] .  generate_config_files:generate_tool_config_xml
[Generating config files] Generating tool configuration XMLs...
[Generating config files] Generating APItool XML...
[Generating config files] Done!
[Generating config files] .  generate_config_files:generate_manifest_jsons
[Generating config files] Generating manifest.json for APItool...
[Generating config files] Done!
[Generating config files] finished
[Generating test files for APItool] started
[Generating test files for APItool] .  Generate tests
[Generating test files for APItool] finished
```

After this command finishes, you will see a file named `apitool.py` under `~/backend/ayx_plugins/` with the boilerplate code. Upon opening the file, you should see something like

```python
class APITool(PluginV2):
    """Concrete implementation of an AyxPlugin."""

    def __init__(self, provider: AMPProviderV2) -> None:
        self.provider = provider
        # truncated init code

    def on_incoming_connection_complete(self, anchor: namedtuple) -> None:
        # on_incoming_connection_complete code

    def on_record_batch(self, batch: "Table", anchor: namedtuple) -> None:
        # input tool doesn't get batches

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
        self.provider.io.info("APITool tool done.")
```

## Writing an API request
Now you are ready to begin modifying this plugin code to pull data from an API and tell the plugin to output it! We will use the [requests](https://requests.readthedocs.io/en/latest/) library to do this.