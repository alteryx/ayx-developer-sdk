File Provider
=============

The File Provider lets you test a Python SDK tool independent of Alteryx
Designer.

Installation
------------

Perform these steps to set up your environment correctly:

1.  Activate the base virtual environment.
2.  Run `pip install /path/to/ayx-sdks/gitrepo`.

The -e flag (for example, `pip install -e/path/to/ayx-sdks/gitrepo`)
installs in editable mode so that changes made to the repo are
automatically reflected.

Input File Formats
------------------

The File Provider needs 4 types of input files to run.

### Tool Configuration File

The tool configuration file contains user input information. In
Designer, this information is normally chosen through the SDK\'s UI, but
in the File Provider these values are set in this configuration file.

An empty configuration file contains only a `Configuration` tag, and a
configuration file with user input has a tag corresponding to each value
that a user sets. See the example below.

```xml
<Configuration>
    <Value>10</Value>
</Configuration>
```

### Workflow Configuration File

Each kind of example tool has its own XML configuration file. The file
contains tool information like name, description, input anchors, and
output anchors. The input and output anchor information is found under
the `InputConnections` and `OutputConnections` tags respectively. Each
`Connection` corresponds to 1 anchor. If the `AllowMultiple` flag is
`True` then there can be multiple connections attached to that anchor.

### Metadata File

The metadata XML file contains information about each field of the
incoming data. Each field must have a `name`, `size`, and `type`.

-   `name`: The field name.
-   `size`: The size of each piece of data in that field.
-   `type`: The type of each piece of data in that field.

`type` must correspond to 1 of the values in the `FieldType` enum. See
the example below:

```xml
<RecordInfo>
  <Field name="Name" size="254" type="v_string" />
  <Field name="Value" size="254" type="double" scale="2" description="the value" source="internet"/>
</RecordInfo>
```

### Record File

The record CSV file contains all of the record information. It looks
like a CSV file that Designer might use as input. The first row should
contain field names corresponding to the name of each field in the
metadata file. The rest of the rows should contain the record data. See
the example below:

```cs
Name,Value
Ten,10
Twenty,20
Thirty,30
```

Running the File Provider
-------------------------

The file provider is run from a command-line argument. The only argument
the user must pass in is a path to a JSON file with this format:

1.  `tool`: This is a dictionary with 2 keys: `plugin` and `path`.

     -   `plugin`: Contains a string that corresponds to the class
         plugin name.
     -   `path`: Contains a string that corresponds to the folder that
         contains the plugin, in other words,
         `{"plugin": "Example", "path": "path/to/ExampleFolder"}`.

2.  `tool\_config`: This is a string that corresponds to the absolute
    path of the tool\'s configuration file, in other words,
    `path/to/ExampleToolConfig.xml`.
3.  `workflow\_config`: This is a string that corresponds to the
    absolute path of the workflow\'s configuration file, in other words,
    `path/to/ExampleWorkflowConfig.xml`.
4.  `inputs`: This is a list of dictionaries that contain information
    about the tool\'s input connections. It is optional since not all
    tools have input. The user should specify input information for each
    input connection that is associated with this tool. Each input
    dictionary has 3 keys: `anchor_name`, `records`, and `metadata`.

     -   `anchor_name`: Contains a string that corresponds to the name
         of the input connection\'s anchor, which has to match an input
         anchor name from the associated configuration file.
     -   `records`: Contains a string that corresponds to the absolute
         path of the input connection\'s record file.
     -   `metadata`: Contains a string that corresponds to the absolute
         path of the input connection\'s metadata file, in other words,
         `{"anchor_name": "AnchorName", "records": "path/to/InputRecords.csv", "metadata": "path/to/InputMetadata.xml"}`.

5.  `outputs`: This is a list of dictionaries that specify where the
    tool\'s output anchor information should be stored. It is optional
    since not all tools have output. The user should specify output
    information for each output anchor that is associated with this
    tool. Each output dictionary has 3 keys: `anchor_name`, `records`,
    and `metadata`.

     -   `anchor_name`: Contains a string that corresponds to the name
         of the output anchor, which has to match an output anchor name
         from the associated configuration file.
     -   `records`: Contains a string that corresponds to the absolute
         path of where the output anchor record information should be
         stored.
     -   `metadata`: Contains a string that corresponds to the absolute
         path of where the output anchor\'s metadata file should be
         stored, in other words,
         `{"anchor_name": "AnchorName", "records": "path/to/OutputRecords.csv", "metadata": "path/to/OutputMetadata.xml"}`.

6.  `update\_tool\_config`: This is an optional path to the updated tool
    configuration file. If the tool\'s configuration changes as the
    plugin is running, then the tool configuration file must be updated
    and sent to an output configuration file. This specifies where the
    updated configuration file should be stored.

### Command Line Options

-   `ayx_plugin_sdk run --tool path\to\InputInfo.json`
-   `python -m ayx_plugin_sdk run --tool path\to\InputInfo.json`
-   In ayx\_plugin\_sdk folder:
    `python __main__.py run --tool path\to\InputInfo.json`

### JSON File Format for Tools with Input Anchors, Input Connections, and Output Anchors

This is an input JSON file for a tool with 2 input anchors, where the
first input anchor has 2 input connections connected to it and the
second input anchor has 1 input connection connected to it. The tool
also has 2 output anchors. Each output anchor always has one output file
associated with it. This must correspond with the anchor information in
`WorkflowConfig.xml`. Note that in JSON, backslashes have to be escaped
for any absolute file paths.

```json
{
  "tool":{
    "plugin":"ComplexExample",
    "path":"examples/ComplexExample"
  },
  "tool_config":"path/to/ToolConfig.xml",
  "workflow_config":"path/to/WorkflowConfig.xml",
  "inputs":[
    {
      "anchor_name":"Input1",
      "records":"path/to/Input11Records.csv",
      "metadata":"path/to/Input11Metadata.xml"
    },
    {
      "anchor_name":"Input1",
      "records":"path/to/Input12Records.csv",
      "metadata":"path/to/Input12Metadata.xml"
    },
    {
      "anchor_name":"Input2",
      "records":"path/to/Input2Records.csv",
      "metadata":"path/to/Input2Metadata.xml"
    }
  ],
  "outputs":[
    {
      "anchor_name":"Output1",
      "records":"path/to/Output1Records.csv",
      "metadata":"path/to/Output1Metadata.xml"
    },
    {
      "anchor_name":"Output2",
      "records":"path/to/Output2Records.csv",
      "metadata":"path/to/Output2Metadata.xml"
    }
  ]
}
```

### JSON File Format for an Output Tool

An output tool should have 1 input anchor and no output anchors.

```json
{
  "tool":{
    "plugin":"OutputExample",
    "path":"examples/OutputExample"
  },
  "tool_config":"path/to/ToolConfig.xml",
  "workflow_config":"path/to/WorkflowConfig.xml",
  "inputs":[
    {
      "anchor_name":"Input",
      "records":"path/to/InputRecords.csv",
      "metadata":"path/to/InputMetadata.xml"
    }
  ]
}
```

### JSON File Format for an Input Tool

An input tool should have 1 output anchor and no input anchors.

```json
{
  "tool":{
    "plugin":"InputExample",
    "path":"examples/InputExample"
  },
  "tool_config":"path/to/ToolConfig.xml",
  "workflow_config":"path/to/WorkflowConfig.xml",
  "outputs":[
    {
      "anchor_name":"Output",
      "records":"path/to/OutputRecords.csv",
      "metadata":"path/to/OutputMetadata.xml"
    }
  ]
}
```

### JSON File Format with an Updated Tool Configuration File

This tool has 1 input anchor and 1 output anchor. It also specifies
where an updated tool configuration file should go.

```json
{
  "tool":{
    "plugin":"InputExample",
    "path":"examples/InputExample"
  },
  "tool_config":"path/to/ToolConfig.xml",
  "workflow_config":"path/to/WorkflowConfig.xml",
    "inputs":[
    {
      "anchor_name":"Input",
      "records":"path/to/InputRecords.csv",
      "metadata":"path/to/InputMetadata.xml"
    }
  ],
  "outputs":[
    {
      "anchor_name":"Output",
      "records":"path/to/OutputRecords.csv",
      "metadata":"path/to/OutputMetadata.xml"
    }
  ],
  "update_tool_config":"path/to/OutputToolConfig.xml"
}
```
