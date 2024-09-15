Differences Between the New and Old Python SDKs
===============================================

Packaging
---------

The original [Alteryx Python
SDK](https://help.alteryx.com/current/developer-help/python-engine-sdk)
was built around a Python package called `AlteryxPythonSDK`. This
package is available at runtime inside of Alteryx Designer, and can be
accessed via import.

The new Python SDK is a standalone Python `pip` package that can be
installed via `pip install`. It doesn\'t depend on any special libraries
that only ship with Designer. Given that it is now standalone, we took
measures to allow tool development outside of Designer.

Getting Started
---------------

Getting started in the old SDK typically means looking at an example
plugin, copying the code and file structure, and then modifying it to
suit your own needs. The new SDK provides a command-line interface (CLI)
that takes care of all of this project setup. Go to the [documentation](../howto/getting_started_markdown.md) for more information.

Development
-----------

In the original Python SDK, the back end of a tool is developed via a
class definition that satisfies the interface described in the [AYX
Plugin Python
Class](https://help.alteryx.com/current/developer-help/ayxplugin-python-class)
article.

This class implements certain methods like `pi_init`,
`pi_add_incoming_connection`, etc. This paradigm leads to lots of
boilerplate code, and makes plugin development a burden on the
developer. This typically leads to the meat of the plugin to be only a
few lines of Python, while the overall tool definition is hundreds of
lines.

To alleviate this problem, the new SDK simplifies the interface that
must be satisfied, to a bare minimum set of requirements.

Similar to the original SDK, in the new SDK, you must write a
`Plugin` class. In the new SDK, a base class definition of `Plugin` is
defined to be used as a parent. This gives you a level of
comfort that you have implemented all necessary methods to have a valid
Alteryx Designer plugin.

Additionally, in the original SDK, a class called `IncomingInterface`
was required. This requirement was removed in the new SDK, as incoming
interfaces and connections are handled behind the scenes by the SDK, and
made available to you via the new `Provider` concept.

Deployment
----------

Once plugin development is complete, the plugin is often distributed via
the YXI file format. You can find the instructions for packaging a YXI in the
original SDK at [Package a Tool](https://help.alteryx.com/current/developer-help/package-tool).
This packaging process was significantly simplified by the new
SDK CLI, described in the [Getting
Started](../howto/getting_started_markdown.md)
guide.