
#### Python SDK v2

Version 2 of AYX Python SDK is now available. For the best experience,
and to ensure compatibility with the most recent versions of Designer,
please use v2 of AYX Python SDK.

-   To learn more about v2 of the AYX Python SDK, go to [Changes and
    Improvements to Python SDK in
    v2.0.0](./differences_with_original_sdk_markdown.md).
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
