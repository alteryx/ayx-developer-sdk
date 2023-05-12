# Test Client

#### AYX SDK CLI

The `ayx-sdk-cli` is the newest addition to the Alteryx Developer
Experience product suite. It currently contains the Test Client and is
the next iteration of the CLI. The `ayx-sdk-cli` houses all the
functionality for Desktop and future Cloud Developer Experience
offerings.

Please note that the `ayx-plugin-cli` is still required for plugin
development until the `ayx-sdk-cli` has matured.

Get the latest release of `ayx-sdk-cli` with the Test Client at
[https://github.com/alteryx/ayx-developer-sdk/releases](https://github.com/alteryx/ayx-developer-sdk/releases).


The Test Client allows you to test SDK tools in a given workspace. You
don\'t need to create and install a YXI for use by Alteryx Designer.
Just give the client a set of inputs and outputs as appropriate, and see
if the plugin runs as expected!

## Anchor Types

-   input
    -   none
    -   single-connection: One input source.
    -   multi-connection: Multiple input sources.
    -   optional (single\|multi): None, or some input sources.
-   output
    -   none
    -   multi-connection: Every output anchor in Alteryx supports
        multiplexing to numerous tools and resources. For the test
        client case, it\'s only 1 output source.

## Supported File Types

-   CSV (\*.csv)
-   JSON (\*.json)
-   NDJSON (\*.ndjson)

#### Note on JSON

Alteryx Designer can write JSON as a JSON Array (\*.json). Other
utilities, like the Apache Arrow library, write JSON as
[NDJSON](http://ndjson.org/) (\*.ndjson) (New Line Delimited).


### JSON (Array)

    [
        {
            "Field1": 1,
            "Field2": 2,
            "Field3": 3
        },
        {
            "Field1": 4,
            "Field2": 5,
            "Field3": 6
        },
        {
            "Field1": 7,
            "Field2": 8,
            "Field3": 9
        }
    ]

### NDJSON

    { "Field1": 1, "Field2": 2, "Field3": 3 }
    { "Field1": 4, "Field2": 5, "Field3": 6 }
    { "Field1": 7, "Field2": 8, "Field3": 9 }

## Command Syntax

`ayx-sdk-cli.exe plugin run [WORKSPACE_PATH]::[PLUGIN_NAME] [--input [--schema]]... --output...`

## Workspace Path and Plugin Name

Run a plugin (passthrough) inside a workspace directory:

`ayx-sdk-cli.exe plugin run Passthrough --input input.csv --output output.csv`

Run a plugin (passthrough) in another directory:

`ayx-sdk-cli.exe plugin run C:\...\...\...\BaseTools::Passthrough --input input.csv --output output.csv`

## Anchor Syntax

The anchor syntax is fairly simple. In some cases, you only need to
provide a path to the filename. In other cases, you might need to supply
the anchor it\'s going to and potentially a format. The test client
tries its best to take any given file and read and write it correctly
based on its file extension. Sometimes this is not possible (reading
from stdin or writing to stdout with no file extension available).

If the anchor only has 1 input or output anchor, the test client
successfully binds any sources to it (based on \--input or \--output
flags). In all other cases, you must supply an anchor name with
`@ANCHOR_NAME` syntax. Just to be sure, a multi-connection tool has a
single anchor but allows multiple connections, so
`--input file.csv --input file.csv --input file.csv` works (only 1 input
anchor is available, named \"Input\").

If you forget to supply enough inputs or outputs, supply too many, or
supply an incorrect anchor name, the test client detects this early and
generates an error. This is also the case if you forget to specify a
type for input and output types like stdin and stdout.

### Examples

#### Example 1

These are examples of the test client that is satisfied with the syntax
(Passthrough tool):

    ayx-sdk-cli.exe Passthrough --input input.csv --output output.csv
    ayx-sdk-cli.exe Passthrough --input input.csv:json --output output.csv:json             // parses as JSON!
    ayx-sdk-cli.exe Passthrough --input input.csv:json --output output.csv:ndjson           // parses as NDJSON!
    ayx-sdk-cli.exe Passthrough --input input.csv:csv@Input --output output.csv:csv@Output
    ayx-sdk-cli.exe Passthrough --input input.csv@Input --output output.csv@Output
    ayx-sdk-cli.exe Passthrough --input input.csv:csv@Input --output :csv                   // stdout
    ayx-sdk-cli.exe Passthrough --input input.csv:csv@Input --output stdout:csv             // also stdout
    ayx-sdk-cli.exe Passthrough --input input.csv:csv@Input --output stdout:csv@Output      // also stdout

#### Example 2

These are examples of the test client that is not satisfied with the
syntax (Passthrough tool):

    ayx-sdk-cli.exe Passthrough --input input.csv --input input2.csv --output.csv           // too many inputs
    ayx-sdk-cli.exe Passthrough --input input.csv --output input.csv                        // input and output sources cannot be the same
    ayx-sdk-cli.exe Passthrough --input input.csv:json --output.csv:json@Output2            // Output2 is non-existent
    ayx-sdk-cli.exe Passthrough --input input.csv:csv@Input --output stdout                 // needs format
    ayx-sdk-cli.exe Passthrough --input input.csv:csv@Input --output stdout@Output          // needs format

#### Example 3

These are examples of something unusual, like the Optional tool:

    ayx-sdk-cli.exe Optional --input input.csv --output output.csv       // ok
    ayx-sdk-cli.exe Optional --output output.csv                         // also ok
    ayx-sdk-cli.exe Optional --input input.csv --output input.csv        // input/output cannot share sources

#### Example 4

These are examples of the test client with a Multi-Connection tool:

    ayx-sdk-cli.exe MultiConnection 
        --input input.csv --input input.csv --input input.csv --input input.csv --input input.csv 
        --output output_one.csv@Output1 --output output_two.csv@Output2 --output output_three.csv@Output3 --output output_four.csv@Output4 --output output_five.csv@Output5     // ok!, input gets auto-mapped (multi-connection, but one anchor)
    ayx-sdk-cli.exe MultiConnection 
        --input input.csv --input input.csv --input input.csv --input input.csv --input input.csv 
        --output output_one.csv@Output1 --output output_two.csv@Output2 --output output_three.csv@Output3 --output output_four.csv@Output4                                      // error! forgot Output5!
    ayx-sdk-cli.exe MultiConnection 
        --input input.csv --input input.csv --input input.csv --input input.csv --input input.csv 
        --output output_one.csv@Output1 --output output_two.csv@Output2 --output output_three.csv@Output3 --output output_four.csv@Output4 --output output_five.csv@Output6     // error! no Output 6!


## Advanced Usage

Piping from stdin to stdout.

    cat some_file.txt | ayx-sdk-cli.exe Passthrough --input :csv --output :csv
    ...
    1,2,3
    4,5,6
    7,8,9
    ...

Contents of **some_file.txt**:

    1,2,3
    4,5,6
    7,8,9

This doesn\'t require a schema:
-  stdin is valid. It can be shared amongst any inputs, like a file.
-  stdount is not valid. Similar to a file, multiple outputs can\'t write to it.

### Example
    cat some_file.txt | ayx-sdk-cli.exe Passthrough 
        --input :csv
        --input :csv
        --input :csv
        --input :csv
        --input :csv
        --output :csv@Output1
        --output :csv@Output2
        --output :csv@Output3
        --output :csv@Output4
        --output :csv@Output5



## Command Reference 
Go to [Test Client Command Reference](./test-client.md) for detailed information.
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
Client](./test-client.md).

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
