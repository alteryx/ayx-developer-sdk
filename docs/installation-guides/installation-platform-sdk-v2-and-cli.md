# Alteryx Platform SDK V2 and CLI Setup
This page describes how to install the Alteryx Platform SDK and Alteryx Plugin CLI.

## Prerequisites
* To use the Alteryx Plugin CLI, your virtual environment must have [Node 14](https://nodejs.org/dist/v14.9.0/). Install Node 14 via the instructions below.
* Alteryx Designer is not required to use the Alteryx Plugin CLI and create plugins, however, you will need a valid installation of [Designer](https://www.alteryx.com/) to use them.
* Test your plugins with the Test Client available in the [ayx-sdk-cli](https://github.com/alteryx/ayx-developer-sdk/releases).

## Set Up the Development Environment
####  Dev Environment Setup
* Download and install [Miniconda](https://docs.conda.io/en/latest/miniconda.html).
* Open an Anaconda Prompt to create a new virutal environment:
```
conda create -n MyEnvName python=3.8.5 nodejs=14 doit
```
* Activate the environment:
```
conda activate MyEnvName
```
Go to [Anaconda Documentation](https://docs.anaconda.com/anaconda/user-guide/getting-started/) for more details.

#### Install the Alteryx Platform SDK and Alteryx Plugin CLI
In the activated virtual environment, pip install the Alteryx Platform SDK and Alteryx Plugin CLI with these commands:
```
pip install ayx_python_sdk
pip install ayx_plugin_cli
```
