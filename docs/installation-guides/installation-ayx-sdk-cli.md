# Alteryx Test Client
This document describes how to install the Alteryx SDK CLI that you can use to test extensions.

## Downloads
The Altyerx SDK CLI is available in the Alteryx Developer SDK. Download the latest versions from the [Releases](https://github.com/alteryx/ayx-developer-sdk/releases) section of the [Alteryx Developer SDK Github Repo](https://github.com/alteryx/ayx-developer-sdk).

## Installation
To install, extract the SDK archive to a directory of your choice, install required [dependencies](#dependencies), and finally, proceed to any platform specific [post installation steps](#post-installation) below.

## Dependencies
Python version 3.8.5 is currently required to use `ayx-sdk-cli.exe plugin run`. We recommended that you install this in a [Miniconda environment](#creating-a-miniconda-python-environment).

### Creating a Miniconda Python Environment
1. Follow the [Miniconda installation](https://docs.conda.io/en/latest/miniconda.html) instructions.
2. From a terminal, create a new environment with Python 3.8.5:

```powershell
conda create -n MyEnvName python=3.8.5
```

> :information_source: Note that if you are using the same Conda environment for `ayx_plugin_cli`, you might want to also install Node.js v14.x and `doit`. For example:
```powershell
conda create -n MyEnvName python=3.8.5 nodejs=14 doit
```

Please refer to the [AYX Python SDK v2](https://help.alteryx.com/developer-help/ayx-python-sdk-v2) documentation for more information on `ayx_plugin_cli` and Python SDK v2 tool development.

## Post Installation
### Windows
In a terminal, change directories to `tools\win32\misc` and run `./setup-sdk.ps1`.

> :information_source: You need to close and restart your terminal after you run this script.

## Additional Reading
Find additional resources in the docs directory available in [releases](https://github.com/alteryx/ayx-developer-sdk/releases).
