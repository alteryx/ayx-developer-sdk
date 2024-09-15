# AYX Plugin CLI

### Overview

The AYX Plugin CLI provides a single mechanism to guide you through the
entire SDK development process, from scaffolding to packaging. It lets
you create tools quickly, familiarize yourself with the SDKs, and it
reduces the potential for error.

### Requirements and Prerequisites

To start building tools with the AYX Plugin CLI, you need these items
installed on your machine:

-   Microsoft Windows 7 or Later (64-bit)
-   Alteryx Designer Version 2021.2 and Later
-   Python Version 3.8.5
-   [pip](=https://pypi.org/)
    (automatically installed with Python 3.8.5)

Each SDK also has its own requirements, which are listed on each
respective help page.

We highly recommend that you develop your custom tools inside of a
virtual environment (for example,
[Miniconda](https://docs.conda.io/en/latest/miniconda.html).
With Miniconda, you can create and activate a virtual environment with
these commands:

`conda create -n SDKEnv python=3.8.5`

`conda activate SDKEnv`

This creates an isolated development environment that minimizes the risk
of creating a package that Alteryx Designer and other users won\'t be
able to use. It keeps the dependencies that different projects require separate.

### Installation

To install the AYX Plugin CLI, run `pip install ayx_plugin_cli`.

#### Verify Installation

To verify that you installed the CLI properly, run
`ayx_plugin_cli version`.

If the installation was successful this command returns the version
number. If the CLI was not installed properly, the `ayx_plugin_cli`
command will not be recognized in the terminal, and your terminal will
reflect that.

### CLI Versions

To check the version of the CLI that is installed, run
`ayx_plugin_cli version`.

The CLI automatically checks for the newest version and alerts you if a
new version is available.

To upgrade the CLI version, run `pip install ayx_plugin_cli --upgrade`.

#### CLI Version Support

We will support the latest version of the CLI. Visit [Release
Notes](https://help.alteryx.com/developer-help/ayx-python-sdk-release-notes) to review new features as well as fixed and known
issues.

### Uninstall

To uninstall the CLI, run `pip uninstall ayx_plugin_cli`.

Once you uninstall the AYX Plugin CLI, you will lose the ability to
manage your custom tool projects. Uninstalling the CLI removes all of
the features that help create, delete, and package custom tools into
YXIs.



# AYX Plugin CLI Commands

Explore the AYX Plugin CLI commands and parameters.

## sdk-workspace-init

This command initializes a workspace---a directory that contains all of
the source code and configuration details for a set of Alteryx SDK
plugins. Users create a workspace to house all of their plugin code, and
once it\'s ready, generate a YXI for said code. The command creates an
`ayx_workspace.json` file that defines package details and tools. It
also generates a `backend/` directory for the plugin code, `config/`
directory for plugin configurations, `ui/` directory for the plugin's UI
components, a README, and a gitignore file.

Note: Most ayx-plugin-cli commands expect an ayx_workspace.json file in
the current directory, and throw an exception otherwise.


### Parameters

Note: If a parameter is not passed in as part of the CLI call, the CLI
waits for standard input for the ignored parameters, even if they're
optional.

#### \--package-name

This parameter becomes the name of the YXI that is generated from the
workspace.

-   Optional or Required: Required
-   Type: String
-   Permissible Values: Any alphanumeric string.

#### \--tool-category

This parameter is the Designer tool category tab that the resulting
tools are placed in when the YXI is installed. If the category does not
exist, one is created when the tool is installed. If left blank, the
tools are installed under the **Python SDK Examples** category.

-   Optional or Required: Optional
-   Type: String
-   Permissible Values: Any
-   Default: Python SDK Examples

#### \--description

The package description.

-   Optional or Required: Optional
-   Type: String
-   Permissible Values: Any

#### \--author

The plugin author.

-   Optional or Required: Optional
-   Type: String
-   Permissible Values: Any

#### \--company

The company creating the plugin.

-   Optional or Required: Optional
-   Type: String
-   Permissible Values: Any

#### \--backend-language

The programming language that a plugin will use. At present, the CLI
only supports Python plugins.

-   Optional or Required: Required
-   Type: String
-   Permissible Values: python

## create-ayx-plugin

This command generates the boilerplate code, configs, and UI for a new
Alteryx plugin in the workspace.

Note: If this command fails midway through execution, it leaves
half-finished files and directories in the workspace. In order to delete
these, follow these steps:

-   Remove config/\<Plugin\> directory.
-   Remove backend/ayx_plugins/\<plugin\>.py.
-   Force-remove ui/\<Plugin\>.
-   Remove the import statement from \_\_init\_\_.py.
-   Remove the tool from ayx_workspace.json's "tools" key.

### Parameters

Note: If a parameter is not passed in as part of the CLI call, the CLI
waits for standard input for the ignored parameters, even if they're
optional.

#### \--tool-name

This parameter becomes the name of the tool. Spaces are allowed but are cleaned into underscores and Pascal
case. For example, for a Python
plugin named "A Test Tool", the filename is `a_test_tool.py`, and the
`class/ui/config` name is `ATestTool`.

-   Optional or Required: Required
-   Type: String
-   Permissible Values: Any alphanumeric string that doesn't start with
    a number and doesn't shadow reserved names.

#### \--tool-type

This parameter is used to determine the scaffold that the tool should
generate for a plugin.

-   Optional or Required: Optional
-   Type: String
-   Permissible Values: input, output, multiple-inputs,
    multiple-outputs, single-input-single-output
-   Default: single-input-single-output

#### \--description

The plugin description.

-   Optional or Required: Optional
-   Type: String
-   Permissible Values: Any

#### \--version

The plugin version.

-   Optional or Required: Optional
-   Type: String
-   Permissible Values: Any

#### \--omit-ui

Don't generate UI artifacts for this plugin. You can generate UI artifacts later with the `generate-ui` command.

## create-yxi

This command packages a workspace into a YXI that can be installed into
Designer. The resulting YXI is located under `build/yxi/`.

### Parameters

#### \--omit-ui

Don't build any UI artifacts for the plugins in the workspace.

- If a plugin doesn't have any UI artifacts, nothing happens.
- If a plugin has UI artifacts, but it was never built, nothing happens.
- If a plugin has UI artifacts and was previously built, the previous build result is packaged.

## install-yxi

This command takes a YXI (any CLI-built or legacy SDK YXI) and installs
it into Designer.

Note: You can run this command from anywhere, not just Alteryx Workspace
directories.

### Parameters

Note: If a parameter is not passed in as part of the CLI call, the CLI
waits for standard input for the ignored parameters, even if they're
optional.

#### \--yxi-path

The location of the YXI to be installed. Note that this does not work
for YXIs built for the original Alteryx Python SDK.

-   Optional or Required: Required
-   Type: String
-   Permissible Values: Any valid path to a YXI.

#### \--install-type

This parameter is used to determine where a plugin should be installed.
Note that admin installation requires admin access.

-   Optional or Required: Required
-   Type: String
-   Permissible Values: user, admin
-   Default: user

## designer-install

This command builds the YXI from the current workspace and installs it
into Designer.

### Parameters

Note: If a parameter is not passed in as part of the CLI call, the CLI
waits for standard input for the ignored parameters, even if they're
optional.

#### \--install-type

This parameter is used to determine where a plugin should be installed.
Note that admin installation requires admin access.

-   Optional or Required: Required
-   Type: String
-   Permissible Values: user, admin
-   Default: user

#### \--omit-ui

Go to [`to --omit-ui`` for --create-yxi](#create-yxi).

## generate-config-files

This command generates and updates the workspace config XML, individual
tool config XMLs, and the tool's `manifest.json` file.

### Parameters

This command takes no parameters.

## generate-ui

This command generates the UI artifacts for the workspace, or a specific plugin.

### Parameters

#### \--tool-name

Generate UI artifacts for a specific plugin.


## Sample ayx_workspace.json

	{
		"name": "TestTools",
		"tool_category": "Test Tools",
		"package_icon_path": "configuration\\default_package_icon.png",
		"author": "John Doe",
		"company": "Alteryx, Inc",
		"copyright": "2021",
		"description": "A sample Alteryx Workspace",
		"ayx_cli_version": "0.1b2.dev0",
		"backend_language": "python",
		"backend_language_settings": {
			"python_version": "3.8",
			"requirements_local_path": "tool_backends\\requirements-local.txt",
			"requirements_thirdparty_path": "tool_backends\\requirements-thirdparty.txt"
		},
		"tools": {
			"TestTool": {
				"backend": {
					"tool_module": "ayx_plugins",
					"tool_class_name": "TestTool"
				},
				"ui": {},
				"configuration": {
					"long_name": "Test Tool",
					"description": "",
					"version": "10.1",
					"search_tags": [],
					"icon_path": "configuration\\TestTool\\icon.png",
					"input_anchors": {
						"Input": {
							"label": "",
							"allow_multiple": false,
							"optional": false
						}
					},
					"output_anchors": {
						"Output": {
							"label": "",
							"allow_multiple": false,
							"optional": false
						}
					}
				}
			}
		},
		"tool_version": "1.0"
	}



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

To initialize the plugin workspace, run `sdk-workspace-init`. You need to define these items:


-   Package Name: The name of the folder where you will create tools.
-   Tool Category: The Alteryx Designer tool category where all of the
    tools in this workspace will appear.
-   Description: This information is presented to the user when they
    install a YXI.
-   Author: Who wrote the plugins?
-   Company: What company owns these plugins?
-   Back-end Language: Currently, Python is the only option.

#### Add Plugin

Once your workspace is ready, run `create-ayx-plugin`. You need
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

:information_source:

Use the `--omit-ui` argument if this plugin doesn't have a UI. You can generate the UI later with the [generate-ui](#generate-ui) command.

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
