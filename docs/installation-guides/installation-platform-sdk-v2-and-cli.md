# Alteryx Platform SDK V2 and CLI Setup
This page describes how to install the Alteryx Platform SDK and Alteryx Plugin CLI.

## Prerequisites
* To use the Alteryx Plugin CLI, your virtual environment must have [Node 14](https://nodejs.org/dist/v14.9.0/). Install Node 14 via the instructions below.
* Alteryx Designer is not required to use the Alteryx Plugin CLI and create plugins, however, you will need a valid installation of [Designer](https://www.alteryx.com/) to use them.
* Test your plugins with the Test Client available in the [ayx-sdk-cli](https://github.com/alteryx/ayx-developer-sdk/releases).

## Set Up the Development Environment
####  Dev Environment Setup
* Install [Python 3.13](https://www.python.org/downloads/) if you haven't already. The installer registers with the [Python Launcher for Windows](https://docs.python.org/3/using/windows.html#python-launcher-for-windows) (`py`).
* Create a new virtual environment pinned to Python 3.13:
```
py -3.13 -m venv MyEnvName
```
> :information_source: The `py` launcher resolves to the latest 3.13.x release installed on your machine. To confirm the exact patch version inside the environment, activate it and run `python --version`.
* Activate the environment:
  * **Command line:** `MyEnvName\Scripts\activate`
  * **VSCode:** Open the Command Palette (`Ctrl+Shift+P`/`Cmd+Shift+P`), run **Python: Select Interpreter**, and choose the interpreter inside `MyEnvName` (for example, `MyEnvName\Scripts\python.exe`).
  * **PyCharm:** Go to **Settings** > **Project** > **Python Interpreter** > **Add Interpreter** > **Add Local Interpreter** > **Existing**, and select the `python` executable inside your `MyEnvName` virtual environment.
* With the environment activated, install [Node 14](https://nodejs.org/dist/v14.9.0/) separately (it's not a pip package), and install `doit` with `pip install doit`.

#### Install the Alteryx Platform SDK and Alteryx Plugin CLI
In the activated virtual environment, pip install the Alteryx Platform SDK and Alteryx Plugin CLI with these commands:
```
pip install ayx_python_sdk
pip install ayx_plugin_cli
```
