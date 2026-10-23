# Alteryx Test Client
This document describes how to install the Alteryx SDK CLI that you can use to test extensions.

## Downloads
The Altyerx SDK CLI is available in the Alteryx Developer SDK. Download the latest versions from the [Releases](https://github.com/alteryx/ayx-developer-sdk/releases) section of the [Alteryx Developer SDK Github Repo](https://github.com/alteryx/ayx-developer-sdk).

## Installation
To install, extract the SDK archive to a directory of your choice, install required [dependencies](#dependencies), and finally, proceed to any platform specific [post installation steps](#post-installation) below.

## Dependencies
Python version 3.13 is currently required to use `ayx-sdk-cli.exe plugin run`. We recommend that you install this in a [Python virtual environment](#creating-a-python-virtual-environment).

### Creating a Python Virtual Environment
1. Install [Python 3.13](https://www.python.org/downloads/) if you haven't already.
2. Create and activate a virtual environment named `MyEnvName` using one of these methods:
   - **Command line:**
     - Verify that `python` resolves to a 3.13.x installation: `python --version`.
     - If you have multiple Python versions installed and the default `python` isn't 3.13.x, run `where python` to list every installation on your `PATH`, then run `<path>\python.exe --version` on each until you find the one reporting 3.13.x.
     - Create the environment with that interpreter:
       ```powershell
       python -m venv MyEnvName
       ```
       (or `"<path-to-python3.13>\python.exe" -m venv MyEnvName` if you had to disambiguate above).
     - Activate it with `MyEnvName\Scripts\activate`.
   - **VSCode:**
     - Open the Command Palette (`Ctrl+Shift+P`/`Cmd+Shift+P`), and run **Python: Create Environment**.
     - Select **Venv**, and choose your Python 3.13 interpreter from the list (VSCode shows the version next to each interpreter, so this works even with multiple installs).
     - VSCode creates the environment and activates it as the workspace interpreter.
     - To activate an existing environment instead of creating a new one, open the Command Palette, run **Python: Select Interpreter**, and choose the venv's `python.exe` (for example, `MyEnvName\Scripts\python.exe`).
   - **PyCharm:**
     - If you're starting a new PyCharm project, you can create the environment directly from the **New Project** screen: set **Interpreter type** to **Project venv**, choose your Python 3.13 version from the dropdown, and click **Create**. PyCharm creates the venv in the project root and sets it as the project interpreter.
     - For an existing project, go to **Settings** > **Project** > **Python Interpreter** > **Add Interpreter** > **Add Local Interpreter** > **Virtualenv Environment** (New).
     - Choose your Python 3.13 interpreter as the base (PyCharm lists the version for each), and confirm.
     - PyCharm creates the environment and sets it as the project interpreter.
     - To activate an existing environment instead, use **Add Interpreter** > **Add Local Interpreter** > **Virtualenv Environment** > **Existing**, and select the `python` executable inside it.

> :information_source: Note that if you are using the same virtual environment for `ayx_plugin_cli`, you might also want to install Node.js v14.x separately and `doit` via `pip install doit`.

Please refer to the [AYX Python SDK v2](https://help.alteryx.com/developer-help/ayx-python-sdk-v2) documentation for more information on `ayx_plugin_cli` and Python SDK v2 tool development.

## Post Installation
### Windows
In a terminal, change directories to `tools\win32\misc` and run `./setup-sdk.ps1`.

> :information_source: You need to close and restart your terminal after you run this script.

## Additional Reading
Find additional resources in the docs directory available in [releases](https://github.com/alteryx/ayx-developer-sdk/releases).
