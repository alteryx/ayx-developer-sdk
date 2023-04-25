# Creating a Workspace
A Workspace is a directory containing information about one or more SDK produced plugins to be packaged into a single, deployable `.yxi` archive. A given Workspace contains a `ayx_workspace.json`, and all other necessary components to build plugins.

To create a Workspace, we first create a new, empty directory. Then, we run the sdk-workspace-init command inside that directory and fill out the prompts, which starts the workspace initialization process.

```bash
~$ mkdir MyWorkspace
~$ cd MyWorkspace
~/MyWorkspace$ ayx_plugin_cli sdk-workspace-init
Package Name: MyPackage
Tool Category [Python SDK Examples]: Python SDK Examples
Description []: My Package
Author []: Alteryx
Company []: Alteryx
Backend Language (python): python
[Workspace initialization] started
[Workspace initialization] .  Create configuration directory
[Workspace initialization] .  Create DCM Schemas directory
...omitted...
Created Alteryx workspace in directory: ~\MyWorskpace
Workspace settings can be modified in: ayx_workspace.json
[Generating config files] started
[Generating config files] .  generate_config_files:generate_config_xml
[Generating config files] Generating top level config XML file...
[Generating config files] finished
```

Next: [Creating a Plugin](create-a-plugin.md)
