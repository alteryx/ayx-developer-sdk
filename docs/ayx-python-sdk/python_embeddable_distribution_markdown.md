Python Embeddable Distribution (PED)
====================================

Python Distribution
-------------------

In the original Python Engine SDK, Alteryx Designer uses a Miniconda
installation with virtual environments to run Python SDK plugins.
However, this results in a folder that is 2.5 GB and contains 86,000
files. The Designer install now comes with an embedded Python
distribution (about 15 MB) that is used by Designer\'s out-of-process
manager to run the Python SDK Plugin, which is now bundled as a `shiv`
artifact.

Packaging Python SDK Plugin and Creating YXI
--------------------------------------------

To leverage the PED, we bundle the Python SDK plugins into a `.pyz` file
using `shiv`, which you can run directly with the PED. The `.pyz` format
is a Python zipapp, part of PEP 441.

To package the plugin workspace, use the SDK command
`ayx_plugin_cli create-yxi`. Once you create the YXI, you can install it
and use it from Designer. The command `ayx_plugin_cli designer-install`
packages the YXI and installs the plugin for you. The plugins inside of
the YXI have a `manifest.json` file that dictates which Python version
Designer uses to run the Python SDK Plugin. For now, the version is set
to 3.8, but support for more versions will be added in the future.

**External Links**

-   <http://legacy.python.org/dev/peps/pep-0441/>
-   <https://docs.python.org/3/using/windows.html#windows-embeddable>
