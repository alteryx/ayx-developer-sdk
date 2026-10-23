# Alteryx Developer SDK

## Downloads
The latest SDK versions can be downloaded from the [Alteryx Developer SDK GitHub Repo](https://github.com/alteryx/ayx-developer-sdk) in the [Releases](https://github.com/alteryx/ayx-developer-sdk/releases) section.
## Installation
To install, extract the SDK archive to a directory of your choice, install required [dependencies](#dependencies), and finally, proceed to any platform specific [post installation steps](#post-installation) below.

### Windows Installation Example

**Via PowerShell**
```powershell
# Download the latest release
# This is an example! Update the URL to the correct archive!
Invoke-Webrequest -URL https://github.com/alteryx/ayx-developer-sdk/releases/download/v2022.12.0/ayx-sdk-cli-v2022.12.0-x86_64-pc-windows-msvc.zip -Outfile latest-sdk.zip

# Extract somewhere
Expand-Archive -Path latest-sdk.zip -DestinationPath C:\SDKs\Alteryx\
```

## Dependencies
Python version 3.13 is currently required to use `ayx-sdk-cli.exe plugin run`. It is recommended to install this in a [Python virtual environment](#creating-a-python-virtual-environment).

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

> :information_source: Note that if you are using the same virtual environment for use with `ayx_plugin_cli`, you may wish to also install Node.js v14.x separately and `doit` via `pip install doit`.

Please refer to the [AYX Python SDK v2](https://help.alteryx.com/developer-help/ayx-python-sdk-v2) documentation for more information on `ayx_plugin_cli` and Python SDK v2 tool development.

## Post Installation
### Windows
In a terminal change directories to the `tools\win32\misc` and run `./setup-sdk.ps1`.

> :information_source: You will need to close and re-open your terminal after running this script.

## Additional Reading
Additional reading can be found within the `docs` directory found within [releases](https://github.com/alteryx/ayx-developer-sdk/releases).

## License
[LICENSE](LICENSE.txt)