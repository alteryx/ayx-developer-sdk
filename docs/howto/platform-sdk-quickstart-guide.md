# Platform SDK Quickstart Guide

#### Python SDK v2

Version 2 of AYX Python SDK is now available. For the best experience,
and to ensure compatibility with the most recent versions of Designer,
please use v2 of [AYX Python
SDK.](https://help.alteryx.com/developer-help/ayx-python-sdk-v2)

-   To learn more about v2 of the AYX Python SDK, go to [Changes and
    Improvements to Python SDK in
    v2.0.0](https://help.alteryx.com/developer-help/changes-and-improvements-python-sdk-v2).
-   If you need to access v1 documentation, you can [download the
    content](https://help.alteryx.com/sites/default/files/2022-02/1.0_0.zip).

The steps below illustrate how to use the latest developer tools to
create a custom plugin or tool for use in Alteryx. For more information
about new SDKs and their usage within Alteryx, please visit [Platform
SDK](https://help.alteryx.com/developer-help/platform-sdk).

### Requirements and Prerequisites

Before you get started, make sure that these items are installed on your
machine:

-   Microsoft Windows 7 or Later (64-bit)
-   Alteryx Designer Version 2021.2\*
-   Python Version 3.8.5
-   [pip](https://pypi.org/) (automatically installed with Python 3.8.5)
-   [node](https://nodejs.org/en/download/) [14](https://nodejs.org/en/blog/release/v14.17.3/)
-   [Git](https://git-scm.com/downloads)

\*Alteryx Designer version 2021.4 is required to use the Alteryx Python
SDK v2.0.0.

### CLI

The AYX Plugin CLI provides you with a set of utilities to manage your
plugin and is a great starting point for building a tool. AYX Python SDK
installation is also covered in this section.

Follow these steps to get started with the CLI:

1.  Run this command to install the AYX Plugin CLI:\
    \
    `pip install ayx-plugin-cli`\
     
2.  To verify that you installed the CLI properly, run this command:\
    \
    `ayx_plugin_cli version`\
    \
    If the installation was successful the above command returns the
    version number. If the CLI was not installed properly, the
    `ayx_plugin_cli` command is not recognized in the terminal, and your
    terminal reflects that.\
     
3.  Run this command to install the AYX Python SDK:\
    \
    `pip install ayx-python-sdk`\
    \
    *(Optional) Create a new directory to house all of your workspaces
    and plugins, and continue the steps in this guide from the new
    directory. This helps keep your folder structure clean.*\
     
4.  Once the installation is successful, run this command to create a
    workspace:\
    \
    `ayx_plugin_cli sdk-workspace-init`\
    \
    The command asks you to provide information about your workspace
    through a series of prompts.\
     
5.  Once you have stepped through the above command, run this command to
    create a custom tool or plugin:\
    \
    `ayx_plugin_cli create-ayx-plugin`\
    \
    The command asks you to provide information about your tool or
    plugin through a series of prompts. Note that this operation can
    take a minute to complete.

Once you have stepped through the above command, you can go to the
location of your workspace and view the files that were created for the
new plugin.

For more information about the CLI, please visit the [reference
documents](https://help.alteryx.com/developer-help/ayx-plugin-cli-overview).

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

#### Warning
V1 of AYX Python SDK is only compatible with Alteryx Designer versions
2021.2 and 2021.3. For the best experience, and to ensure compatibility
with the most recent versions of Designer, please use [version 2 of AYX
Python
SDK](https://help.alteryx.com/developer-help/ayx-python-sdk-v2).

To learn more about version 2 of the AYX Python SDK, go to [Changes and
Improvements to Python SDK in
v2.0.0](https://help.alteryx.com/developer-help/changes-and-improvements-python-sdk-v2).


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
documents](https://help.alteryx.com/developer-help/ayx-python-sdk) or access the full [Python
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
