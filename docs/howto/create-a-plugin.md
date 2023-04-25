# Creating a Plugin
After [creating a Workspace](create-a-workspace.md), we can add a Plugin. To do so, use the create-ayx-plugin command. Reply to the prompts and then you will have the template code for your SDK Plugin. For this tool, we use the Input tool type.

```bash
~/MyWorkspace$ ayx_plugin_cli create-ayx-plugin
Tool Name: My Plugin
Tool Type (input, multiple-inputs, multiple-outputs, optional, output, single-input-single-output, multi-connection-input-anchor) [single-input-single-output]: input
Description []: My Plugin
Tool Version [1.0]: 1.0
DCM Namespace []:
Creating input plugin: My Plugin
[Create plugin] started
[Create plugin] Downloading UI components via git
[Create plugin] Cloning into '.ayx_cli.cache\ui_tool_template'...
[Create plugin] .  Create plugin
[Create plugin] Installing UI components via npm
[Create plugin] Creating Alteryx Plugin...
[Create plugin] Copying example tool to ~\MyWorkspace\backend\ayx_plugins...
...omitted...
[Generating config files] finished
[Generating test files for APItool] started
[Generating test files for APItool] .  Generate tests
[Generating test files for APItool] finished
```
