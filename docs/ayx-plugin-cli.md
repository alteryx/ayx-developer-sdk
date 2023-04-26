# AYX Plugin CLI

### Overview

The AYX Plugin CLI provides a single mechanism to guide you through the
entire SDK development process, from scaffolding to packaging. It lets
you create tools quickly, familiarize yourself with the SDKs, and it
reduces the potential for error.

### Requirements and Prerequisites

To start building tools with the AYX Plugin CLI, you need these items
installed on your machine:

-   Microsoft Windows 7 or Later (64-bit)
-   Alteryx Designer Version 2021.2 and Later
-   Python Version 3.8.5
-   [pip](=https://pypi.org/)
    (automatically installed with Python 3.8.5)

Each SDK also has its own requirements, which are listed on each
respective help page.

We highly recommend that you develop your custom tools inside of a
virtual environment (for example,
[Miniconda](https://docs.conda.io/en/latest/miniconda.html).
With Miniconda, you can create and activate a virtual environment with
these commands:

`conda create -n SDKEnv python=3.8.5`

`conda activate SDKEnv`

This creates an isolated development environment that minimizes the risk
of creating a package that Alteryx Designer and other users won\'t be
able to use. It does this by keeping the dependencies required by
different projects separate.

### Installation

To install the AYX Plugin CLI, run `pip install ayx_plugin_cli`.

#### Verify Installation

To verify that you installed the CLI properly, run
`ayx_plugin_cli version`.

If the installation was successful this command returns the version
number. If the CLI was not installed properly, the `ayx_plugin_cli`
command will not be recognized in the terminal, and your terminal will
reflect that.

### CLI Versions

To check the version of the CLI that is installed, run
`ayx_plugin_cli version`.

The CLI automatically checks for the newest version and alerts you if a
new version is available.

To upgrade the CLI version, run `pip install ayx_plugin_cli --upgrade`.

#### CLI Version Support

We will support the latest version of the CLI. Visit [Release
Notes](https://help.alteryx.com/developer-help/ayx-python-sdk-release-notes) to review new features as well as fixed and known
issues.

### Uninstall

To uninstall the CLI, run `pip uninstall ayx_plugin_cli`.

Once you uninstall the AYX Plugin CLI, you will lose the ability to
manage your custom tool projects. Uninstalling the CLI removes all of
the features that help create, delete, and package custom tools into
YXIs.
