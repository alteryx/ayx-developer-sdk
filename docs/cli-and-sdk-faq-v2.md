# CLI and SDK FAQ in v2
:::

::: node--info
::: node--info--modified
Last modified: December 19, 2022
:::
:::

::: {.paragraph .paragraph--type--compound-accordion-group .paragraph--view-mode--default}
::: {.clearfix .text-formatted .field .field--name--field-top-content .field--type--text-long .field--label--hidden}
Explore frequently asked questions about the new Platform SDK.
:::

::: {.accordion responsive-accordion-tabs="accordion" allow-all-closed="true" multi-expand="true"}
::: {.accordion-item accordion-item=""}
[Why does the CLI use Python?](#){.accordion-title}

::: {.accordion-content tab-content=""}
::: {.clearfix .text-formatted .field .field--name--field-information .field--type--text-long .field--label--hidden}
Since we were already developing a Python SDK, it made sense to use
Python for the CLI, too. Python lets us leverage the [doit automation
tool](../../external.html?link=https://pydoit.org/ "https://pydoit.org/"){rel="noopener"
target="_blank"} to build the CLI. We chose to use
[Typer](../../external.html?link=https://typer.tiangolo.com/ "Typer"){rel="noopener"
target="_blank"} in combination with doit because it lets us map CLI
commands to doit tasks.
:::
:::
:::

::: {.accordion-item accordion-item=""}
[Can I use the CLI and SDK behind a firewall?](#){.accordion-title}

::: {.accordion-content tab-content=""}
::: {.clearfix .text-formatted .field .field--name--field-information .field--type--text-long .field--label--hidden}
#### Do I need to whitelist anything to use the CLI?

To download and install the CLI, be notified of a newer version of the
CLI, or check for updates to the CLI, you need to whitelist
[https://pypi.org/](../../external.html?link=https://pypi.org/ "https://pypi.org/"){target="_blank"}.
Otherwise, feel free to use the CLI completely offline.

#### What packages do I need to download?

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
:::
:::
:::

::: {.accordion-item accordion-item=""}
[Why another Python SDK?](#){.accordion-title}

::: {.accordion-content tab-content=""}
::: {.clearfix .text-formatted .field .field--name--field-information .field--type--text-long .field--label--hidden}
The original [Python Engine
SDK](python-engine-sdk.html "Python Engine SDK"){entity-substitution="canonical"
entity-type="node" entity-uuid="76296a9f-df4c-4332-b73f-2b5c10a2eba1"
target="_blank"} is complex, runs in-process, and can be slow. The [AYX
Python SDK](ayx-python-sdk.html) design solves these issues. It runs
out-of-process using gRPC to communicate. It also simplifies the
development process of new tools to 4 function calls, abstracting away a
lot of the previous SDK function calls.

By running the plugin out-of-process, we are able to efficiently manage
multiple plugins and are not bound by the restrictions of the C++
`boost` library.
:::
:::
:::

::: {.accordion-item accordion-item=""}
[Python Engine SDK and AYX Python SDK. What's the
difference?](#){.accordion-title}

::: {.accordion-content tab-content=""}
::: {.clearfix .text-formatted .field .field--name--field-information .field--type--text-long .field--label--hidden}
[AYX Python
SDK](ayx-python-sdk-v2.html "AYX Python SDK"){entity-substitution="canonical"
entity-type="node" entity-uuid="1ef0d76b-18c7-4132-832c-4364753c6223"
rel="noopener" target="_blank"} is a new SDK product. It improves upon
the original Python Engine SDK by providing a consistent development
experience moving forward. While the Python Engine SDK was designed to
use the original engine, the new AYX Python SDK leverages the brand new
[AMP
Engine](../20223/designer/alteryx-amp-engine.html "AMP Engine"){entity-substitution="canonical"
entity-type="node" entity-uuid="e13022bf-27e2-45b6-ae25-0210fe3706a8"
rel="noopener" target="_blank"}.
:::
:::
:::

::: {.accordion-item accordion-item=""}
[Are there any changes to packaging between the Python Engine SDK and
AYX Python SDK?](#){.accordion-title}

::: {.accordion-content tab-content=""}
::: {.clearfix .text-formatted .field .field--name--field-information .field--type--text-long .field--label--hidden}
In the new SDK, we switched from using packaged up virtual environments
to python zip apps. We believe this update provides an overall positive
change because now tools with different environments work on the same
tool canvas (no virtual environment collisions).

Please note that this might change how you packaged up, distributed, and
tested your plugins.
:::
:::
:::

::: {.accordion-item accordion-item=""}
[Do I need Alteryx Designer to build and test a
plugin?](#){.accordion-title}

::: {.accordion-content tab-content=""}
::: {.clearfix .text-formatted .field .field--name--field-information .field--type--text-long .field--label--hidden}
Alteryx Designer is not required to build a custom plugin. However,
Designer is required to test a plugin and make sure that it works
correctly.
:::
:::
:::

::: {.accordion-item accordion-item=""}
[What IDE should I use?](#){.accordion-title}

::: {.accordion-content tab-content=""}
::: {.clearfix .text-formatted .field .field--name--field-information .field--type--text-long .field--label--hidden}
We recommend [Visual Studio
Code](../../external.html?link=https://code.visualstudio.com/ "Visual Studio Code"){target="_blank"}
or
[PyCharm](../../external.html?link=https://www.jetbrains.com/pycharm/ "PyCharm"){target="_blank"}.
:::
:::
:::

::: {.accordion-item accordion-item=""}
[What's the purpose of the AYX Plugin CLI?](#){.accordion-title}

::: {.accordion-content tab-content=""}
::: {.clearfix .text-formatted .field .field--name--field-information .field--type--text-long .field--label--hidden}
The AYX Plugin CLI provides a single mechanism to guide you through the
entire SDK development process, from scaffolding to packaging. It lets
you create tools quickly, familiarize yourself with the SDKs, and it
reduces the potential for error.

The CLI facilitates the process of custom tool creation for any SDK.
*Note that at this time it only supports Python.*\
 
:::
:::
:::

::: {.accordion-item accordion-item=""}
[What's the difference between sdk-workspace-init and create-ayx-plugin
commands?](#){.accordion-title}

::: {.accordion-content tab-content=""}
::: {.clearfix .text-formatted .field .field--name--field-information .field--type--text-long .field--label--hidden}
-   `sdk-workspace-init`: This command initializes a workspace directory
    --- think of this as a project playground where all your custom
    plugins exist. The workspace directory will be setup with a
    pre-defined folder structure which enables the rest of the CLI
    commands to properly function.
-   `create-ayx-plugin`: This command adds a plugin to the workspace.
    You must choose a template tool type and specify a tool name.
:::
:::
:::

::: {.accordion-item accordion-item=""}
[I see a \"Can\'t find plugin SdkEnginePlugin.dll\" error message, what
do I do?](#){.accordion-title}

::: {.accordion-content tab-content=""}
::: {.clearfix .text-formatted .field .field--name--field-information .field--type--text-long .field--label--hidden}
If you encounter the \"Can't find plugin SdkEnginePlugin.dll\" error,
[enable the AMP Engine
runtime](../20223/designer/alteryx-amp-engine.html#how-to-switch-on-amp "enable the AMP engine runtime"){target="_blank"}
in Alteryx Designer. To do so\...

1.  In Alteryx Designer, access the **Workflow - Configuration** window.
2.  Select the **Runtime** tab.
3.  Check the check box to **Use AMP Engine**.\
     

    ::: {.embedded-entity embed-button="image_embed" entity-embed-display="entity_reference:media_image" entity-type="media" entity-uuid="fb415d6e-39cf-47ab-9d5f-2159a673ccd3" langcode="en"}
    ![Thumbnail](../sites/default/files/image/2021-03/enable-amp-engine.png "Enable AMP Engine"){width="500"
    height="553" loading="lazy" typeof="foaf:Image"}
    :::
:::
:::
:::

::: {.accordion-item accordion-item=""}
[How do I customize the icon for a new Alteryx tool
category?](#){.accordion-title}

::: {.accordion-content tab-content=""}
::: {.clearfix .text-formatted .field .field--name--field-information .field--type--text-long .field--label--hidden}
This is not done directly via the SDK, however, you can customize the
icon via these instructions:

1.  Find an icon you would like to use for the tool category. The icon
    must be in PNG format.
2.  Rename the icon file to match the tool category name
    *exactly.* Remove any spaces and punctuation from the file name. For
    example, \"New Tools\" becomes \"NewTools\".
3.  Place the file in the folder that contains the Alteryx icons:
    [C:\\Program
    Files\\Alteryx\\bin\\RuntimeData\\icons\\categories]{.path}.
4.  Restart Designer.
:::
:::
:::

::: {.accordion-item accordion-item=""}
[I use SDK version 2.0.0 and see an \"InboundPipeError\" message. What
do I do?](#){.accordion-title}

::: {.accordion-content tab-content=""}
::: {.clearfix .text-formatted .field .field--name--field-information .field--type--text-long .field--label--hidden}
You might receive this error if you have an incorrect version of the
protobuf library in the setup for your AYX Python plugin. To address the
error\...

1.  Please go to the directory that contains the
    [ayx_workspace.json]{.path} file for your Python SDK plugin.
2.  Next, go to the \\backend sub-folder and add this line to the
    [requirements-thirdparty.txt]{.path} file: `protobuf==3.20.1`.
3.  Rebuild the plugin.