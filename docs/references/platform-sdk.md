# Platform SDK

The Platform SDK is a modern superset of the capabilities available in
the former [Engine and HTML GUI
SDKs](https://help.alteryx.com/developer-help/legacy-sdks). Previous SDKs use outdated technology and limit
extension opportunities. The new SDKs use the latest open-source
technology and open up new ways to extend Alteryx products.

### Overview

The Platform SDK lets you extend your Alteryx experience by building
custom tools and plugins.

While Alteryx Designer provides a wide range of functionality with the
available tools, you might find that you perform a specific action or
task that could be better served by creating a custom tool or plugin.
You can distribute custom tools within your organization and environment
and still leverage the speed and flexibility of Designer and Server.

A custom tool or plugin consists of 2 components:

1.  The user interface, shown in Designer's Configuration window. To
    create the user interface component, use the [AYX UI
    SDK](https://alteryx.github.io/alteryx-ui/)
    (a React-based front-end SDK that lets you build custom applications
    to use within the Alteryx platform).
2.  The engine, which processes logic to handle records passed to and
    from the Alteryx Engine. To create the engine component, use the
    [AYX Python
    SDK](./ayx-python-sdk-v2.md).

To help facilitate the creation of a custom tool or plugin, you can
leverage the [AYX Plugin
CLI](./ayx-plugin-cli.md).
This command-line tool walks you through generating the set of files and
folders needed for your custom project. The CLI includes commands for
common tasks like packaging the tool for deployment.

#### Engine Compatibility

The Platform SDK requires that the [AMP
Engine](https://help.alteryx.com/20223/designer/alteryx-amp-engine) is enabled.

### Requirements and Prerequisites

To start building tools with the AYX Plugin CLI, you need these items
installed on your machine:

-   Microsoft Windows 7 or Later (64-bit)
-   Alteryx Designer Version 2021.2
-   Python Version 3.8.5
-   [pip](https://pypi.org/) (automatically installed with Python 3.8.5)

Each SDK also has its own requirements, which are listed on each
respective help page below.

### SDK Quickstart Guide

Visit the [Platform SDK Quickstart
Guide](../howto/platform-sdk-quickstart-guide.md) to learn how to use the latest developer tools to
create a custom plugin or tool for use in Alteryx.