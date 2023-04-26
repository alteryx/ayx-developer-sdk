# Test Client Command Reference

## Using Help

The test client itself offers help at any stage of the program. Just
include `--help` where it\'s needed.

#### Help from the Root

`ayx-sdk-cli.exe --help`

#### Help from Sub-Commands

    ayx-sdk-cli.exe extension --help    # help for extension
    ayx-sdk-cli.exe plugin --help       # help for plugin
    ayx-sdk-cli.exe plugin run --help   # help for plugin/run
    ayx-sdk-cli.exe self --help         # help for self

## Global Settings

#### assume-yes

Specify this to answer yes to all prompts and run non-interactively.

#### thread-pool-size

Specify the number of threads to be used by the test client. The default
is the number of CPU/cores on the machine. You might want to adjust this
if important tasks are being run in the background.

## Logging

This configures the logging options. You can specify log output to
stdout or file. The default format is Human but you can specify other
formats, such as Bunyan or JSON, as well.

The default logging level is INFO, which is what should be used most of
the time. Other logging levels are more verbose, such as TRACE, DEBUG,
and WARN ERROR.

#### log-facility

Log to stdout or file (default is stdout).

#### log-file

Output location of a file log. If the file already exists, the test
client appends to it.

#### log-format

The test client supports human-readable (default),
[Bunyan](https://github.com/trentm/node-bunyan), and JSON.

#### log-level

Set the log level for the test client. By default this is INFO. Some
levels might be extremely verbose.

##### INFO (default)
    ayx-sdk-cli.exe plugin run BaseTools\::Passthrough --input input.csv --output test.csv
    2022-10-17T19:34:50.144008Z  INFO ayx_sdk_cli::cli: User invocation command="ayx-sdk-cli.exe plugin run BaseTools\\::Passthrough --input input.csv --output test.csv"
    ...
    2022-10-17T19:34:50.151119Z  INFO ayx_sdk_cli::commands::plugin::run: Extension loaded extension="Passthrough v2.0.0 (runtime target: ayx-sdk-extension-python-3_8_5)"
    2022-10-17T19:34:50.153458Z  INFO ayx_sdk_cli::commands::plugin::run: Async threadpool threadpool_size=16
    2022-10-17T19:34:50.164368Z  INFO plugin_execution: ayx_sdk_cli::plugin::tool_process: Extension runtime spawned runtime_pid=11592

##### DEBUG
    /ayx-sdk-cli.exe plugin run BaseTools\::Passthrough --input input.csv --output output.csv --log-level debug
    2022-10-17T18:57:02.814839Z  INFO ayx_sdk_cli::cli: User invocation command="ayx-sdk-cli.exe plugin run BaseTools\\::Passthrough --input input.csv --output test.csv --log-level debug"
    ...
    2022-10-17T18:57:02.822777Z DEBUG plugin_execution: ayx_sdk_cli::plugin::tool_process: Spawning extention runtime... command="python"
    ...
    2022-10-17T18:57:02.826512Z DEBUG plugin_execution: ayx_sdk_cli::commands::plugin::run::tool_service: Attempting to acquire extension runtime tool service port assignment...
    2022-10-17T18:57:03.602284Z  INFO plugin_execution: ayx_sdk_cli::commands::plugin::run::tool_service: Acquired port from runtime tool service tool_service_port=53241
    2022-10-17T18:57:03.602301Z  INFO plugin_execution: tool_client: Connecting to extension runtime tool service tool_service_address="http://localhost:53241"


## Commands

### Completion

#### list

Show the available list of shells for which the test client can provide
an auto-completion script.

    ayx-sdk-cli.exe completion list
    Bash
    Zsh
    PowerShell
    Elvish
    ...

#### show

Provide the auto-completion script for a given shell.

Step 1: Create a new completion file.

`ayx-sdk-cli.exe completion show powershell > $profile/ayx-sdk-cli-completions.ps1`

Step 2: Add the following to the end of `$profile`.

`. $PSScriptRoot\ayx-sdk-cli-completions.ps1`

### Extension

#### list

List extensions found in the current workspace.

    ayx-sdk-cli.exe extension list
    ...
    Found 9 extension(s):
    - ConversionPassthrough v1.0.0 (runtime target: ayx-sdk-extension-python-3_8_5)
    - Input v2.0.0 (runtime target: ayx-sdk-extension-python-3_8_5)
    - Optional v2.0.0 (runtime target: ayx-sdk-extension-python-3_8_5)
    - Passthrough v2.0.0 (runtime target: ayx-sdk-extension-python-3_8_5)
    - MultipleInputs v2.0.0 (runtime target: ayx-sdk-extension-python-3_8_5)
    - DcmInput v1.0.0 (runtime target: ayx-sdk-extension-python-3_8_5)
    - MultiConnection v2.0.0 (runtime target: ayx-sdk-extension-python-3_8_5)
    - MultipleOutputs v2.0.0 (runtime target: ayx-sdk-extension-python-3_8_5)
    - Output v2.0.0 (runtime target: ayx-sdk-extension-python-3_8_5)


#### extension

Provide information about a specific extension.

    ayx-sdk-cli.exe extension info Passthrough
    ...
    Name           : Passthrough
    Package Name   : N/A
    Description    : An example single-input-single-output tool. This tool takes data from the input anchor and, without changing it, writes it to the output anchor.
    Kind           : com.alteryx.sdk.tool
    Version        : 2.0.0
    Runtime Target : ayx-sdk-extension-python-3_8_5
    Category       : Python SDK Examples
    Copyright      : 2022


### Plugin

#### run

Runs a given set of inputs against an SDK plugin. Shows any messages
from the plugin in stdout, including responses. Writes any outputs to
the specified outputs given.

`ayx-sdk-cli.exe plugin run [WORKSPACE_PATH]::[PLUGIN_NAME] --input <[SOURCE][:TYPE[:OPTIONS]][@ANCHOR]> --output <[DESTINATION][:TYPE[:OPTIONS]][@ANCHOR]> --runtime-command`

For more information, go to [Test
Client](https://help.alteryx.com/developer-help/test-client).

### Self

#### update

Updates the test client to the latest version.

    ayx-sdk-cli.exe self update
    ...
    Checking target-arch... x86_64-pc-windows-msvc
    Checking current version... v2022.7.1
    Checking latest released version...
    ...

### Version

Displays the test client version.

    ayx-sdk-cli.exe version
    ayx-sdk-cli 2022.7.1
    ...
