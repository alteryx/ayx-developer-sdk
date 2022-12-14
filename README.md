# Alteryx Developer SDK

## Downloads
The latest SDK versions can be downloaded from the [Alteryx Developer SDK GitHub Repo](https://github.com/alteryx/ayx-developer-sdk).
## Installation
To install, extract the SDK archive to a directory of your choice, install required [dependencies](#dependencies), and finally, proceed to any platform specific [post installation steps](#post-installation) below.

## Dependencies
Python version 3.8.5 is currently required to use `ayx-sdk-cli.exe plugin run`. It is recommended to install this in a [Miniconda environment](#creating-a-miniconda-python-environment).

### Creating a Miniconda Python Environment
1. Follow the [Miniconda installation](https://docs.conda.io/en/latest/miniconda.html) instructions.
2. From a terminal, create a new environment with Python 3.8.5:

```powershell
conda create -n MyEnvName python=3.8.5
```

> :information_source: Note that if you are using the same Conda environment for use with `ayx_plugin_cli`, you may wish to also install Node.js v14.x and `doit` as seen below:
```powershell
conda create -n MyEnvName python=3.8.5 nodejs=14 doit
```

Please refer to the [AYX Python SDK v2](https://help.alteryx.com/developer-help/ayx-python-sdk-v2) documentation for more information on `ayx_plugin_cli` and Python SDK v2 tool development.

## Post Installation
### Windows
In a terminal change directories to the `tools\win32\misc` and run `./setup-sdk.ps1`.

> :information_source: You will need to close and re-open your terminal after running this script.

## Additional Reading
Additional reading can be found within the `docs` directory found within [releases](https://github.com/alteryx/ayx-developer-sdk/releases).

## License
[LICENSE](LICENSE.txt)