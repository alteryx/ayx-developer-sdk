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
    SDK](#python-sdk-v2).

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

Visit the [Getting Started Guide](../howto/getting_started_markdown.md) to learn how to use the latest developer tools to
create a custom plugin or tool for use in Alteryx.


### Python SDK v2

Version 2 of AYX Python SDK is now available. For the best experience,
and to ensure compatibility with the most recent versions of Designer,
please use v2 of AYX Python SDK.

-   To learn more about v2 of the AYX Python SDK, go to [Changes and
    Improvements to Python SDK in
    v2.0.0](./differences-with-original-sdk-markdown.md).
-   If you need to access v1 documentation, you can [download the
    content](https://help.alteryx.com/sites/default/files/2022-02/1.0_0.zip).


### Overview

The AYX Python SDK lets you extend the functionality of Alteryx Designer
via custom tools and plugins. This SDK serves as the back-end engine
component. Combine it with the [AYX UI
SDK](https://alteryx.github.io/alteryx-ui/) (which serves as the user interface component) to create your custom
tool or plugin.

#### Engine Compatibility

The AYX Python SDK requires that the [AMP
Engine](https://help.alteryx.com/20223/designer/alteryx-amp-engine) is enabled.

### Requirements and Prerequisites

To get started with the AYX Python SDK, you need these items installed
on your machine:

-   Microsoft Windows 7 or Later (64-bit)
-   Python Version 3.8.5
-   Alteryx Designer Version 2021.4

### Installation

To install the AYX Python SDK, run `pip install ayx-python-sdk`.

-   This command provides the AYX Plugin CLI (top-level CLI) as well as
    the AMP Provider classes.
-   The AYX Plugin CLI uses the Python SDK CLI to manage the creation
    and installation of Python tools.

As noted above, you can install the package via
[pip](https://pypi.org/). Any updates to
packages will also be available on pip. You do not need to update or
manage this package directly since it is a dependency of the AYX Plugin
CLI.

### AYX Python SDK Documentation

You can access the AYX Python SDK documentation at
[https://alteryx.github.io/ayx-python-sdk/index.html](https://alteryx.github.io/ayx-python-sdk/index.html).
Additionally, after you install the AYX Python SDK distribution, you can
run `ayx_python_sdk docs` to access the help documentation locally.
