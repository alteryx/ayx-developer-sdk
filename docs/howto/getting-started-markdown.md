Getting Started Guide
=====================

Prerequisites
-------------

- To get started with the Alteryx Platform SDK, you need a valid installation of [Alteryx Designer](https://www.alteryx.com/).
- Python version 3.8.5 is required for Alteryx Designer plugins.

Set Up the Development Environment
----------------------------------

Follow these steps to configure your development environment.

### Create the Virtual Environment

To get started\...

1.  Install [Miniconda3](https://docs.conda.io/en/latest/miniconda.html)
    for your system.
2.  Once the install is done, open an Anaconda Prompt and create a new
    virtual environment: `conda create -n ayx_python_sdk python=3.8.5`.
3.  Next, activate it: `conda activate ayx_python_sdk`.

If you are not familiar with Anaconda/Miniconda, visit [Anaconda
Documentation](https://docs.anaconda.com/anaconda/user-guide/getting-started/).

### Install the Package

After you create and activate your virtual environment, pip install the
Alteryx Platform SDK pip package. For more information on pip, visit the
[pip website](https://pypi.org/).

Use this command to install the SDK:

`pip install ayx-python-sdk`

If you do not already have the Alteryx Plugin CLI, use this command to
install the CLI:

`pip install ayx-plugin-cli`

### Create the Ayx Plugin Workspace

Now that the Alteryx Python SDK is installed in your virtual environment
packages, create a new [Plugin Tool Workspace](#Glossary)
with default files ready to go.

Use this command to create the workspace:
`ayx_plugin_cli sdk-workspace-init`

This initializes a workspace to manage all of your custom tools and
plugins.

To create a new tool, use the `create-ayx-plugin` command.

The `create-ayx-plugin` command takes these parameters:

 -   `--tool-name`: (Required) The name of the new Plugin tool.
 -   `--tool-type`: The type of tool to create.

For this example, name your new tool `MyFirstTool`. Use the
tool-type `single-input-single-output` parameter to create the new tool
with default input and output anchors.

Use this command:

`ayx_plugin_cli create-ayx-plugin`

### Workspace Configuration

When a workspace is created, an `ayx_workspace.json` file is generated
inside of your workspace directory. This file tracks metadata related to
your workspace. By default, you don't need to worry about this file
because the CLI commands manage and update it.

### Create Your Production Installer

After you implement and test your new Ayx Plugin Tool, you
might want to distribute it to others. In order to do this, you must
create a YXI installer. The Core SDK CLI provides a command to
package your workspace and tools into an installer.

Run the `create-yxi` command to generate a YXI installer that is ready
for distribution.

By default, the name of the YXI is based on the Ayx Plugin
Workspace directory name, but you can override the default with the
`--yxi-name` flag. Alternatively, you can modify the `yxi_name` field in
the `ayx_workspace.json` file. (Refer to the [Workspace
Configurations ](#Glossary)
section for details).

### Build the Ayx Plugin Tool

The [sdk-workspace-init]{.title-ref} command sets up the folder
structure with a `backends` folder, `ui` folder, and `configuration`
folder. These folders have all the files necessary for Alteryx Designer
to integrate with your plugin.

Next, you can build your new Ayx Plugin Tool into Designer, where
you can drag it onto the canvas and connect it to other Designer tools.
To build `MyFirstTool` into the Designer application, use the
`designer-install` command.

Use this command to build MyFirstTool into Designer:

`ayx_plugin_cli designer-install`

You just created your first Alteryx Plugin Tool! You can now open
Alteryx Designer and find your new tool in the Tool Palette.

### Ayx Plugin Tool Execution in Designer

When Designer runs a tool, it must look for an engine to use. In the
case of the MyFirstTool Python tool, the engine is itself the *Python
interpreter*. The interpreter is built out of Anaconda and includes all
of the packages indicated in `requirements.txt`.

The ToolFamily defined in the Config.xml file within the Ayx Plugin
Workspace defines the name of the virtual environment created for all of
your Ayx Plugin tools. By default, a ToolFamily is set up for your Ayx
Plugin Workspace for all of your tools to use.

The YXI installation package includes all of the interpreter information
so that the Python interpreter can be recreated on any machine when the
tools are installed.

The `EngineDLLEntryPoint` within the Config.xml file points to the file
that contains a class definition that inherits from `Plugin`. This file
can be changed at any time to any Python file as long as it contains a
`Plugin` class that registers with the Alteryx Core SDK.

-   For a detailed explanation of the Config.xml file, go to [Tool
	Configurations.](../references/config-xml-markdown.md).
-   For information on the main.py file within your Ayx Plugin Tool,
	go to [Plugin Code
	Overview.](../references/plugin-code-markdown.md).

### Configuration Panel GUI

The Alteryx Core SDK examples provide basic Configuration Panel GUIs,
however, the Core SDK only executes the engine (the Python side of the
code). Therefore this Getting Started Guide doesn't cover Alteryx UI
development. For more information on Configuration Panel GUI
development, go to [Alteryx UI
SDK](https://help.alteryx.com/developer-help/ayx-ui-sdk).

## Platform SDK Quickstart Guide

#### Python SDK v2

The steps below illustrate how to use the latest developer tools to
create a custom plugin or tool for use in Alteryx. For more information
about new SDKs and their usage within Alteryx, please visit [Platform SDK](../references/platform-sdk.md).

### Requirements and Prerequisites

Before you get started, make sure that these items are installed on your
machine:

-   Microsoft Windows 7 or later (64-bit)
-   Alteryx Designer Version 2021.2\*
-   Python Version 3.8.5
-   [pip](https://pypi.org/) (automatically installed with Python 3.8.5)
-   [node](https://nodejs.org/en/download/) [14](https://nodejs.org/en/blog/release/v14.17.3/)
-   [Git](https://git-scm.com/downloads)

\*Alteryx Designer version 2021.4 or greater is required to use the Alteryx Python
SDK v2.0.0.

### CLI

The AYX Plugin CLI provides you with a set of utilities to manage your
plugin and is a great starting point for building a tool. AYX Python SDK
installation is also covered in this section.

[Follow these steps to get started with the CLI.](#install-the-package).

For more information about the CLI, please visit the [reference
documents](../references/ayx-plugin-cli.md).

### UI SDK

The UI SDK consists of 2 pieces.

-   The 1st piece is a React-based [component
    library](https://alteryx.github.io/alteryx-ui/)
    that enables you to build the interface for your tool or plugin.
-   The 2nd piece is a [communication
    bridge](https://alteryx.github.io/react-comms/)
    that lets you interact with Alteryx Designer and persists the values
    that you want to save between runs of a workflow, clicking on and
    off a tool. These are also the values that are available to the
    engine (back end) of your tool.

For the real-time Dev Harness that assists in tool UI development, refer to [Dev Harness.](https://github.com/alteryx/dev-harness)

Follow these steps to get started with the UI SDK:

1.  To start on the user interface of your project, navigate to the
    folder that was created for your workspace in the last step of the
    CLI section above. In this workspace folder, there is a UI directory
    for the workspace. There is a folder inside of this directory with
    the same name as the plugin you created.
2.  Navigate to [\[workspace directory\]\\ui\\\[plugin
    name\]\\src\\src]{.path} for the tool you are working on.
3.  Open the index.tsx file. This is the primary
    [React](https://reactjs.org/)
    file for the tool UI.
4.  Make a change to the file. For example, edit the text of a tag, or
    add a [new
    component](https://alteryx.github.io/alteryx-ui/)
    or HTML element to the page.
5.  Save the file.
6.  For a quick preview of your tool in a browser, run this command:\
    \
    `npm run start`
7.  To view your tool in Alteryx Designer, run this command from the
    root workspace directory. This command builds and installs your
    plugin into Designer.\
    \
    `ayx_plugin_cli designer-install`

Open Alteryx Designer, search for your tool, place it on the canvas, and
view the changes.

For more information about the UI SDK, please visit the [reference
documents](https://alteryx.github.io/alteryx-ui/).


### Python SDK


The Python SDK defines the way that you should create the engine/back
end/runtime of your tool. The back end also receives the configuration
values that were created by the front end of the tool in the UI SDK
section.

Follow these steps to get started with the Python SDK:

1.  To start on the engine or runtime of your project, navigate to the
    folder that was created for your workspace in the last step of the
    CLI section above. In this workspace folder, there is a back-end
    directory for the workspace.
2.  Navigate to [\[workspace directory\]\\backend\\ayx_plugins\\\[plugin
    name\].py]{.path} for the tool you are editing.
3.  Make changes to the file.
4.  Save the file.
5.  Run this command from the root workspace directory. This builds and
    installs your plugin into Alteryx Designer.\
    \
    `ayx_plugin_cli designer-install`

Open Alteryx Designer, search for your tool, place it on the canvas, and
view the changes.

For more information about the Python SDK, please go to the [reference
documents](../references/platform-sdk.md) or access the full [Python
SDK documentation](https://alteryx.github.io/ayx-python-sdk/index.html).
You can also access this documentation locally via this command:

`ayx_python_sdk docs`


### Troubleshooting

-   If you get a workflow error that says 'Can\'t find plugin
    \"SdkEnginePlugin.dll\"\', or \"This tool is only supported in the
    AMP Engine. Please enable AMP to use this tool.\", [enable the AMP
    engine](https://help.alteryx.com/20223/designer/alteryx-amp-engine)
    for the workflow.
-   If your tool panel does not render or shows a blank screen, [enable
    Chrome Developer
    Tools](https://help.alteryx.com/developer-help/html-developer-tools).
    Now, when you select your tool a Chrome debugger is presented and
    you can see any errors for the tool interface.


------------------------------------------------------------------------

### Glossary
--------

-   `Ayx Plugin Workspace`: YXI development workspace with
    sub-directories for individual Ayx Plugin Tools and plugin tool
    files. The Ayx Plugin Workspace is also used to create the YXI
    installer.
-   `Ayx Plugin Tool`: An Alteryx Designer custom tool built on the
    Alteryx Core SDK.
-   `YXI`: Packaging file and directory system for Ayx Plugin Tools.
-   `Tool Configuration`: XML configuration file used by both the
    Alteryx Core SDK and Alteryx Designer to read metadata regarding the
    structure of the Ayx Plugin Tool.
-   `Tool Family`: Shared resources for all Ayx Plugin Tools within an
    Ayx Plugin Workspace. Tool Families define the name of the virtual
    environment, indicate to Designer what virtual environment
    interpreter to run for the Ayx Plugin Tool, and contain the
    pip-installed pip packages defined in the `requirements.txt` file.
