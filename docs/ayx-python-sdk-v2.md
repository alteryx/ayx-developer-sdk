
#### Python SDK v2

::: howto--content
Version 2 of AYX Python SDK is now available. For the best experience,
and to ensure compatibility with the most recent versions of Designer,
please use v2 of AYX Python SDK.

-   To learn more about v2 of the AYX Python SDK, go to [Changes and
    Improvements to Python SDK in
    v2.0.0](changes-and-improvements-python-sdk-v2.html "Changes and Improvements to Python SDK in v2.0.0"){entity-substitution="canonical"
    entity-type="node"
    entity-uuid="88eb7663-6b8c-48a6-88f7-f9b0d8625963"
    testid="inline-card-resolved-view" rel="noopener" role="button"
    tabindex="0" target="_blank"}.
-   If you need to access v1 documentation, you can [download the
    content](../sites/default/files/2022-02/1.0_0.zip).
:::
:::

### Overview {#overview .index-item}

The AYX Python SDK lets you extend the functionality of Alteryx Designer
via custom tools and plugins. This SDK serves as the back-end engine
component. Combine it with the [AYX UI
SDK](../../external.html?link=https://alteryx.github.io/alteryx-ui/ "AYX UI SDK"){target="_blank"}
(which serves as the user interface component) to create your custom
tool or plugin.

::: howto
#### Engine Compatibility

::: howto--content
The AYX Python SDK requires that the [AMP
Engine](../20223/designer/alteryx-amp-engine.html "AMP Engine"){entity-substitution="canonical"
entity-type="node" entity-uuid="e13022bf-27e2-45b6-ae25-0210fe3706a8"
target="_blank"} is enabled.
:::
:::

### Requirements and Prerequisites {#requirements-and-prerequisites .index-item}

To get started with the AYX Python SDK, you need these items installed
on your machine:

-   Microsoft Windows 7 or Later (64-bit)
-   Python Version 3.8.5
-   Alteryx Designer Version 2021.4

### Installation {#installation .index-item}

To install the AYX Python SDK, run `pip install ayx-python-sdk`.

-   This command provides the AYX Plugin CLI (top-level CLI) as well as
    the AMP Provider classes.
-   The AYX Plugin CLI uses the Python SDK CLI to manage the creation
    and installation of Python tools.

As noted above, you can install the package via
[pip](../../external.html?link=https://pypi.org/). Any updates to
packages will also be available on pip. You do not need to update or
manage this package directly since it is a dependency of the AYX Plugin
CLI.

### AYX Python SDK Documentation {#ayx-python-sdk-documentation .index-item}

You can access the AYX Python SDK documentation at
[https://alteryx.github.io/ayx-python-sdk/index.html](../../external.html?link=https://alteryx.github.io/ayx-python-sdk/index.html "https://alteryx.github.io/ayx-python-sdk/index.html"){target="_blank"}.
Additionally, after you install the AYX Python SDK distribution, you can
run `ayx_python_sdk docs` to access the help documentation locally.
:::
:::