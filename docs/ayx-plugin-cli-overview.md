# AYX Plugin CLI Overview

### CLI Architecture

The AYX Plugin CLI is a command-line interface based on
[Typer](https://typer.tiangolo.com/),
a tool that helps you build and manage custom plugins for Alteryx
Designer. This top-level CLI oversees the creation and metadata of your
plugins. It delegates the tasks of creating and building YXIs.

The AYX Plugin CLI detects which SDK your workspace is using to develop
plugins and delegates the other CLI commands to their respective SDKs.
For example, if you are developing Python tools, the CLI calls the
Python implementation of `create-ayx-plugin`. However, if you are using
another SDK to develop tools, the CLI delegates the `create-ayx-plugin`
call to that SDK's implementation.

This architecture allows for one CLI to manage the entire workspace,
abstracting away the details of the commands to their respective SDKs.
This lets you develop in different SDK languages without the need to
download multiple CLI tools.

### Exploring the AYX Plugin CLI

You can use the command line to access information on CLI usage, as well
as available commands and their descriptions.

-   **AYX Plugin CLI**: Use the `ayx_plugin_cli` command (with no
    arguments) to open help content for the AYX Plugin CLI (top-level
    CLI).
-   **Python SDK CLI**: Use the `ayx_python_sdk` command (with no
    arguments) to open help content for the Python SDK CLI.

You can also pass in the `--help` argument to display the same
information as described above.

The help menu contains 3 sections:

-   **Usage**: The Usage section describes the order in which commands
    and options are passed.
-   **Options**: The Options section lists the available options and
    their descriptions.
-   **Commands**: The Commands section lists the available commands and
    their descriptions.

### AYX Plugin CLI General Usage

To create a default tool with the AYX Plugin CLI, follow these steps.

#### Initialize Workspace

To initialize the plugin workspace, run `sdk-workspace-init`. You will
be asked to define these items:

-   Package Name: The name of the folder where you will create tools.
-   Tool Category: The Alteryx Designer tool category where all of the
    tools in this workspace will appear.
-   Description: This information is presented to the user when they
    install a YXI.
-   Author: Who wrote the plugins?
-   Company: What company owns these plugins?
-   Back-end Language: Currently, Python is the only option.

#### Add Plugin

Once your workspace is ready, run `create-ayx-plugin`. You will be asked
to define these items:

-   Tool Name: The display name of the tool in Alteryx Designer.
-   Tool Type: This generates a template file for you to start using.
    The options are: `input`, `multiple-inputs`,
    `multiple-outputs`, `output`, and `single-input-single-output`.
-   Description: The text a user sees when they select a tool in the
    Alteryx Designer tool palette.
-   Tool Version: Defaults to 1.0. This allows you to maintain multiple
    versions of a tool so that users can choose to upgrade to a new
    version or use the previous one inside of any Alteryx workflows.

#### Generate YXI

Now that you have added your plugin, run `create-yxi`. This zips up the
folder and saves it as a YXI. To install this in Alteryx Designer,
double-click on the newly created .yxi file or drag the YXI into Alteryx
Designer.

#### Install YXI in Designer

During development, it can be time-consuming to repeatedly repackage and
reinstall a YXI just to test one component that changed. You can use the
`designer-install` command to install tools directly into Alteryx
Designer from the source. This handles package installation and allows
for a more seamless developer testing experience.

### Workspace.json and Config.xml Files

#### Workspace JSON

The ayx-workspace.json file is the source of truth for the SDK
workspace. A workspace essentially describes the set of tools that will
be packaged and distributed. It is also read by the CLI to generate the
top-level Config XML, ToolConfigXMLs, and Package YXI.

The ayx-workspace.json file is generated as part of the workspace
initialization process. The workspace is a project description. It keeps
track of all the tools that have been created, as well as their
properties and metadata. This includes\...

-   Number of Connections
-   Number of Input and Output Anchors
-   Metadata like tool names, version, icon path, etc.

When you add tools to the workspace, this subsequently modifies the
ayx-workspace.json file so that the ayx-workspace.json is *in sync* with
the directory structure and accurately describes the project workspace.

##### Important
In general, you should not modify the ayx-workspace.json file because
it's managed and updated by the CLI commands. If you are an advanced
workspace user and want to modify the file, keep in mind that
modifications can cause unknown errors and unpredictable results.

#### Config XML

The top-level Config XML describes package metadata. The autogenerated
ToolConfigXMLs are used by the Plugin to get and set anchors.

##### ToolConfigXML Files

Do not edit the autogenerated ToolConfigXML files. This could cause
unpredictable results.

### Troubleshooting and Known Limitations

Any errors that the AYX Plugin CLI generates are shown at runtime in the
terminal. They include descriptions to indicate what caused the error.

#### Known Limitations

-   Tool names cannot start with a number and must be alphanumeric.
-   The AYX Plugin CLI currently supports one back-end language
    (Python).
-   If you connect a Python SDK plugin to a Text Input tool with no
    rows, it triggers an unrelated error. To fix this, you need to add
    rows to the Text Input tool.
