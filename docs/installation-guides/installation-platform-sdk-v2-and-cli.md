# Alteryx Platform SDK V2 and CLI Setup
This page describes how to install the Alteryx Platform SDK and Alteryx Plugin CLI.

## Prerequisites
* To use the Alteryx Plugin CLI, your virtual environment must have [Node 14](https://nodejs.org/dist/v14.9.0/). Install Node 14 via the instructions below.
* Alteryx Designer is not required to use the Alteryx Plugin CLI and create plugins, however, you will need a valid installation of [Designer](https://www.alteryx.com/) to use them.
* Test your plugins with the Test Client available in the [ayx-sdk-cli](https://github.com/alteryx/ayx-developer-sdk/releases).

## Set Up the Development Environment
####  Dev Environment Setup
* Install [Python 3.13](https://www.python.org/downloads/) if you haven't already.
* Create and activate a virtual environment named `MyEnvName` using one of these methods:
  * **Command line:**
    * Verify that `python` resolves to a 3.13.x installation: `python --version`.
    * If you have multiple Python versions installed and the default `python` isn't 3.13.x, run `where python` to list every installation on your `PATH`, then run `<path>\python.exe --version` on each until you find the one reporting 3.13.x.
    * Create the environment with that interpreter:
      ```
      python -m venv MyEnvName
      ```
      (or `"<path-to-python3.13>\python.exe" -m venv MyEnvName` if you had to disambiguate above).
    * Activate it with `MyEnvName\Scripts\activate`.
  * **VSCode:**
    * Open the Command Palette (`Ctrl+Shift+P`/`Cmd+Shift+P`), and run **Python: Create Environment**.
    * Select **Venv**, and choose your Python 3.13 interpreter from the list (VSCode shows the version next to each interpreter, so this works even with multiple installs).
    * VSCode creates the environment and activates it as the workspace interpreter.
    * To activate an existing environment instead of creating a new one, open the Command Palette, run **Python: Select Interpreter**, and choose the venv's `python.exe` (for example, `MyEnvName\Scripts\python.exe`).
  * **PyCharm:**
    * If you're starting a new PyCharm project, you can create the environment directly from the **New Project** screen: set **Interpreter type** to **Project venv**, choose your Python 3.13 version from the dropdown, and click **Create**. PyCharm creates the venv in the project root and sets it as the project interpreter.
    * For an existing project, go to **Settings** > **Project** > **Python Interpreter** > **Add Interpreter** > **Add Local Interpreter** > **Virtualenv Environment** (New).
    * Choose your Python 3.13 interpreter as the base (PyCharm lists the version for each), and confirm.
    * PyCharm creates the environment and sets it as the project interpreter.
    * To activate an existing environment instead, use **Add Interpreter** > **Add Local Interpreter** > **Virtualenv Environment** > **Existing**, and select the `python` executable inside it.
* With the environment activated, install [Node 14](https://nodejs.org/dist/v14.9.0/) separately (it's not a pip package), and install `doit` with `pip install doit`.

#### Install the Alteryx Platform SDK and Alteryx Plugin CLI
In the activated virtual environment, pip install the Alteryx Platform SDK and Alteryx Plugin CLI with these commands:
```
pip install ayx_python_sdk
pip install ayx_plugin_cli
```
