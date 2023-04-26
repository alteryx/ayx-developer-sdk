# AYX Plugin CLI Commands

Explore the [AYX Plugin
CLI](https://help.alteryx.com/developer-help/ayx-plugin-cli) commands and parameters.

## sdk-workspace-init {#sdk-workspace-init .index-item}

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
will wait for standard input for the ignored parameters, even if they're
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
will wait for standard input for the ignored parameters, even if they're
optional.

#### \--tool-name

This parameter becomes the name of the tool. Spaces are allowed but will
be cleaned into underscores and Pascal case. For example, for a Python
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

## create-yxi

This command packages a workspace into a YXI that can be installed into
Designer. The resulting YXI is located under `build/yxi/`.

### Parameters

This command takes no parameters.

## install-yxi

This command takes a YXI (any CLI-built or legacy SDK YXI) and installs
it into Designer.

Note: This command can be run from anywhere, not just Alteryx Workspace
directories.

### Parameters

Note: If a parameter is not passed in as part of the CLI call, the CLI
will wait for standard input for the ignored parameters, even if they're
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

## designer-install {#designer-install .index-item}

This command builds the YXI from the current workspace and installs it
into Designer.

### Parameters

Note: If a parameter is not passed in as part of the CLI call, the CLI
will wait for standard input for the ignored parameters, even if they're
optional.

#### \--install-type

This parameter is used to determine where a plugin should be installed.
Note that admin installation requires admin access.

-   Optional or Required: Required
-   Type: String
-   Permissible Values: user, admin
-   Default: user

## generate-config-files {#generate-config-files .index-item}

This command generates and updates the workspace config XML, individual
tool config XMLs, and the tool's `manifest.json` file.

### Parameters

This command takes no parameters.

## Sample ayx_workspace.json {#sample-ayx_workspace.json .index-item}

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