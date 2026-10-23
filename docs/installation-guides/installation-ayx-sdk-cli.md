# Alteryx Test Client
This document describes how to install the Alteryx SDK CLI that you can use to test extensions.

## Downloads
The Altyerx SDK CLI is available in the Alteryx Developer SDK. Download the latest versions from the [Releases](https://github.com/alteryx/ayx-developer-sdk/releases) section of the [Alteryx Developer SDK Github Repo](https://github.com/alteryx/ayx-developer-sdk).

## Installation
To install, extract the SDK archive to a directory of your choice, install required [dependencies](#dependencies), and finally, proceed to any platform specific [post installation steps](#post-installation) below.

## Dependencies
Python version 3.13 is currently required to use `ayx-sdk-cli.exe plugin run`. We recommend that you install this in a [Python virtual environment](#creating-a-python-virtual-environment).

### Creating a Python Virtual Environment
1. Install [Python 3.13](https://www.python.org/downloads/) if you haven't already. The installer registers with the [Python Launcher for Windows](https://docs.python.org/3/using/windows.html#python-launcher-for-windows) (`py`).
2. From a terminal, create a new virtual environment pinned to Python 3.13:

```powershell
py -3.13 -m venv MyEnvName
```

> :information_source: The `py` launcher resolves to the latest 3.13.x release installed on your machine. To confirm the exact patch version inside the environment, activate it and run `python --version`.

3. Activate the environment:
   * **Command line:** `MyEnvName\Scripts\activate`
   * **VSCode:** Open the Command Palette (`Ctrl+Shift+P`/`Cmd+Shift+P`), run **Python: Select Interpreter**, and choose the interpreter inside `MyEnvName` (for example, `MyEnvName\Scripts\python.exe`).
   * **PyCharm:** Go to **Settings** > **Project** > **Python Interpreter** > **Add Interpreter** > **Add Local Interpreter** > **Existing**, and select the `python` executable inside your `MyEnvName` virtual environment.

> :information_source: Note that if you are using the same virtual environment for `ayx_plugin_cli`, you might also want to install Node.js v14.x separately and `doit` via `pip install doit`.

Please refer to the [AYX Python SDK v2](https://help.alteryx.com/developer-help/ayx-python-sdk-v2) documentation for more information on `ayx_plugin_cli` and Python SDK v2 tool development.

## Post Installation
### Windows
In a terminal, change directories to `tools\win32\misc` and run `./setup-sdk.ps1`.

> :information_source: You need to close and restart your terminal after you run this script.

## Additional Reading
Find additional resources in the docs directory available in [releases](https://github.com/alteryx/ayx-developer-sdk/releases).
