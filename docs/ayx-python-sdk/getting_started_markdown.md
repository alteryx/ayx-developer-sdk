Getting Started Guide
=====================

Prerequisites
-------------

To get started with the Alteryx Core SDK, you need a valid installation
of [Alteryx Designer](https://www.alteryx.com/).

Python version 3.8.5 is required for Alteryx Designer plugins.

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
Alteryx Core SDK pip package. For more information on pip, visit the
[pip website](https://pypi.org/).

Use this command to install the SDK:

`pip install ayx-python-sdk`

If you do not already have the Alteryx Plugin CLI, use this command to
install the CLI:

`pip install ayx-plugin-cli`

### Create the Ayx Plugin Workspace

Now that the Alteryx Python SDK is installed in your virtual environment
packages, we\'ll create a new [Plugin Tool
Workspace](https://extensibility.pages.git.alteryx.com/ayx-sdks/getting_started.html#glossary)
with default files ready to go.

Use this command to create the workspace:
`ayx_plugin_cli sdk-workspace-init`

This initializes a workspace to manage all of your custom tools and
plugins.

To create a new tool, use the `create-ayx-plugin` command.

The `create-ayx-plugin` command takes these parameters:

 -   `--tool-name`: (Required) The name of the new Plugin tool
 -   `--tool-type`: The type of tool to create.

For this example we\'ll name our new tool `MyFirstTool`. We\'ll use the
tool-type `single-input-single-output` parameter to create the new tool
with default input and output anchors.

Use this command:

`ayx_plugin_cli create-ayx-plugin`

### Workspace Configuration

When a workspace is created, a `ayx_workspace.json` file is generated
inside of your workspace directory. This file tracks metadata related to
your workspace. By default, you do not need to worry about this file
because it is managed and updated by the CLI commands.

### Create Your Production Installer

After you have implemented and tested your new Ayx Plugin Tool, you
might want to distribute it to others. In order to do this, you must
create a YXI installer. The Core SDK CLI provides a command for
packaging your workspace and tools into an installer.

Run the `create-yxi` command to generate a YXI installer that is ready
for distribution.

By default, the name of the YXI produced is based on the Ayx Plugin
Workspace directory name, but you can override the default with the
`--yxi-name` flag. Alternatively, you can modify the `yxi_name` field in
the `ayx_workspace.json` file. (See the [Workspace
Configurations](https://extensibility.pages.git.alteryx.com/ayx-sdks/python-sdk/getting_started.html#workspace-configurations)
section for details).

### Build the Ayx Plugin Tool

The [sdk-workspace-init]{.title-ref} command sets up the folder
structure with a `backends` folder, `ui` folder, and `configuration`
folder. These folders have all the files necessary for Alteryx Designer
to integrate with your plugin.

Next we\'re going to build your new Ayx Plugin Tool into Designer, where
you can drag it onto the canvas and connect it to other Designer tools.
To build `MyFirstTool` into the Designer application, use the
`designer-install` command.

Use this command to build MyFirstTool into Designer:

`ayx_plugin_cli designer-install`

**Congratulations!**

You just created your first Alteryx Plugin Tool! You can now open
Alteryx Designer and find your new tool in the Tool Palette.

### Ayx Plugin Tool Execution in Designer

When Designer runs a tool, it must look for an engine to use. In the
case of our MyFirstTool Python tool, the engine is itself the *Python
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

-   For a detailed explanation of the Config.xml file, see [Tool
    Configurations](https://extensibility.pages.git.alteryx.com/ayx-sdks/python-sdk/config_xml.html).
-   For information on the `main.py` file within your Ayx Plugin Tool,
    see [Plugin Code
    Overview](https://extensibility.pages.git.alteryx.com/ayx-sdks/python-sdk/plugin_code.html).

### The Configuration Panel GUI

The Alteryx Core SDK examples provide basic Configuration Panel GUIs,
however, the Core SDK *only* executes the engine (the Python side of the
code). Therefore this Getting Started Guide does not cover Alteryx UI
development. For more information on Configuration Panel GUI
development, see [Alteryx UI
SDK](https://help.alteryx.com/developer-help/ayx-ui-sdk).

------------------------------------------------------------------------

Glossary
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
