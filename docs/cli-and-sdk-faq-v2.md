# CLI and SDK FAQ in v2

Explore frequently asked questions about the new Platform SDK.

## Why does the CLI use Python?

Since we were already developing a Python SDK, it made sense to use
Python for the CLI, too. Python lets us leverage the [doit automation
tool](https://pydoit.org/) to build the CLI. We chose to use
[Typer](https://typer.tiangolo.com/) in combination with doit because it lets us map CLI
commands to doit tasks.


## Can I use the CLI and SDK behind a firewall?

### Do I need to whitelist anything to use the CLI?

To download and install the CLI, be notified of a newer version of the
CLI, or check for updates to the CLI, you need to whitelist
[https://pypi.org/](https://pypi.org/).
Otherwise, feel free to use the CLI completely offline.

### What packages do I need to download?

All of the required Python packages that you need to get started with
development are downloaded and installed when you install the CLI and
SDK (as part of their dependencies).

The requirements for each package are:

-   **SDK**: \"Click==7.1.2\", \"grpcio==1.39.0\", \"numpy\>=1.17.1\",
    \"deprecation==2.1.0\", \"pyarrow==5.0.0\", \"pandas==1.1.0\",
    \"protobuf\>=3.5.0.post1\", \"psutil==5.6.3\", \"pydantic==1.8.2\",
    \"python-dateutil==2.8.1\", \"pytz==2020.1\", \"shiv==0.3.1\",
    \"six==1.14.0\", \"typer==0.3.1\", \"xmltodict==0.12.0\",
    \"requests==2.24.0\", PyPAC==0.15.0\"
-   **CLI**: \"typer==0.3.1\", \"doit==0.33.1\", \"pydantic==1.8.2\",
    \"packaging==20.4\", \"requests==2.24.0\", \"xmltodict==0.12.0\"


## Why another Python SDK?

The original [Python Engine
SDK](https://help.alteryx.com/developer-help/python-engine-sdk) is complex, runs in-process, and can be slow. The [AYX
Python SDK](https://help.alteryx.com/developer-help/ayx-python-sdk) design solves these issues. It runs
out-of-process using gRPC to communicate. It also simplifies the
development process of new tools to 4 function calls, abstracting away a
lot of the previous SDK function calls.

By running the plugin out-of-process, we are able to efficiently manage
multiple plugins and are not bound by the restrictions of the C++
`boost` library.


## Python Engine SDK and AYX Python SDK. What's the difference?

[AYX Python SDK](https://help.alteryx.com/developer-help/ayx-python-sdk-v2) is a new SDK product. It improves upon
the original Python Engine SDK by providing a consistent development
experience moving forward. While the Python Engine SDK was designed to
use the original engine, the new AYX Python SDK leverages the brand new [AMP
Engine](https://help.alteryx.com/20223/designer/alteryx-amp-engine).


## Are there any changes to packaging between the Python Engine SDK and AYX Python SDK?

In the new SDK, we switched from using packaged up virtual environments
to python zip apps. We believe this update provides an overall positive
change because now tools with different environments work on the same
tool canvas (no virtual environment collisions).

Please note that this might change how you packaged up, distributed, and
tested your plugins.


## Do I need Alteryx Designer to build and test a plugin?

Alteryx Designer is not required to build a custom plugin. However,
Designer is required to test a plugin and make sure that it works
correctly.


## What IDE should I use?

We recommend [Visual Studio Code](https://code.visualstudio.com/) or [PyCharm](https://www.jetbrains.com/pycharm/).


## What's the purpose of the AYX Plugin CLI?

The AYX Plugin CLI provides a single mechanism to guide you through the
entire SDK development process, from scaffolding to packaging. It lets
you create tools quickly, familiarize yourself with the SDKs, and it
reduces the potential for error.

The CLI facilitates the process of custom tool creation for any SDK.
*Note that at this time it only supports Python.*\


## What's the difference between sdk-workspace-init and create-ayx-plugin commands?

-   `sdk-workspace-init`: This command initializes a workspace directory
    --- think of this as a project playground where all your custom
    plugins exist. The workspace directory will be setup with a
    pre-defined folder structure which enables the rest of the CLI
    commands to properly function.
-   `create-ayx-plugin`: This command adds a plugin to the workspace.
    You must choose a template tool type and specify a tool name.


## I see a \"Can\'t find plugin SdkEnginePlugin.dll\" error message, what do I do?

If you encounter the \"Can't find plugin SdkEnginePlugin.dll\" error,
[enable the AMP Engine
runtime](https://help.alteryx.com/node/9521#how-to-switch-on-amp)
in Alteryx Designer. To do so\...

1.  In Alteryx Designer, access the **Workflow - Configuration** window.
2.  Select the **Runtime** tab.
3.  Check the check box to **Use AMP Engine**.\
     

## How do I customize the icon for a new Alteryx tool category?

This is not done directly via the SDK, however, you can customize the
icon via these instructions:

1.  Find an icon you would like to use for the tool category. The icon
    must be in PNG format.
2.  Rename the icon file to match the tool category name
    *exactly.* Remove any spaces and punctuation from the file name. For
    example, \"New Tools\" becomes \"NewTools\".
3.  Place the file in the folder that contains the Alteryx icons:
    **C:\\Program Files\\Alteryx\\bin\\RuntimeData\\icons\\categories**.
4.  Restart Designer.


## I use SDK version 2.0.0 and see an \"InboundPipeError\" message. What do I do?

You might receive this error if you have an incorrect version of the
protobuf library in the setup for your AYX Python plugin. To address the
error\...

1.  Please go to the directory that contains the
    **ayx_workspace.json** file for your Python SDK plugin.
2.  Next, go to the \\backend sub-folder and add this line to the
    **requirements-thirdparty.txt** file: `protobuf==3.20.1`.
3.  Rebuild the plugin.
