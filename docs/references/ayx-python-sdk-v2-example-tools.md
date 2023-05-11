# AYX Python SDK v2 Example Tools

### Example Tools

These are example tools created using version 2 the [AYX Python
SDK](./ayx-python-sdk-v2.md). When the tools are installed, they display in the SDK
Examples tool category in Alteryx Designer.


#### Back-end Tools

These examples demonstrate back-end tools and are the same as the
template tools available via the CLI. The user interface of the Input
Tool example is interactive but please note that the other user
interfaces in these examples are not interactive.


#### Engine Compatibility

The AYX Python SDK requires that the [AMP
Engine](https://help.alteryx.com/20223/designer/alteryx-amp-engine) is enabled.


### V2 Example Tools {#v2-example-tools .index-item}

#### Download All Example Tools

You can [download a single YXI
file](https://help.alteryx.com/sites/default/files/2022-02/BaseTools.yxi)
that contains all of the example tools, or download the tools
individually via the download links below.

#### Conversion Passthrough Tool

An example single-input-single-output tool. This tool takes an Arrow
Table from the input anchor, converts it into a Pandas DataFrame, and
then converts it back again before it writes it to the output anchor.
You
can [download](https://help.alteryx.com/sites/default/files/2022-02/ConversionPassThrough_0.yxi) and
install this example in Alteryx Designer.

#### DCM Input Tool

An example input tool that connects to DCM via the UI window. You
can [download](https://help.alteryx.com/sites/default/files/2022-02/DcmInputTool_0.yxi) and
install this example in Alteryx Designer. For more about this tool, go
to [DCM Input Example
Tool](./dcm-input-example-tool.md).

#### Input Tool

An example input tool that generates and sends 3 rows of dummy data. You
can [download](https://help.alteryx.com/sites/default/files/2022-02/InputTool_0.yxi) and
install this example in Alteryx Designer.

#### Multi Connection Tool

An example multi-input-multi-output tool. The input anchor can take in
any number of connections but only provides 5 output anchors. The tool
passes the first 4 inputs through to the corresponding output anchors,
then performs a union operation on the rest, and writes those to the
fifth output anchor. You
can [download](https://help.alteryx.com/sites/default/files/2022-02/MultiConnectionTool_0.yxi) and
install this example in Alteryx Designer.

#### Multiple Input Tool

An example multi-input tool. This tool takes in data from 2 input
anchors and then performs a simple union operation on the 2 sets before
it writes them to the output anchor. You
can [download](https://help.alteryx.com/sites/default/files/2022-02/MultipleInputTool_0.yxi) and
install this example in Alteryx Designer.

#### Multiple Output Tool

An example multi-output tool. This tool expects a single integer field
named \"Value\", which it uses to filter the rows into 2 output streams.
The top anchor corresponds to odd values and the bottom anchor
corresponds to even values.You
can [download](https://help.alteryx.com/sites/default/files/2022-02/MultipleOutputTool_0.yxi) and
install this example in Alteryx Designer.

#### Optional Tool

An example optional input tool. When there is an input provided, the
tool acts as a passthrough tool and takes data from the input anchor and
writes it to the output anchor. When there is no input provided, the
tool generates data instead. Note: There is a known bug in optional
tools that causes them to run twice from start to finish and duplicate
rows in the process. You
can [download](https://help.alteryx.com/sites/default/files/2022-02/OptionalTool_0.yxi) and
install this example in Alteryx Designer.

#### Output Tool

An example output tool. This tool takes an input data table and outputs
information about the table\'s metadata to Designer\'s Results window.
You
can [download](https://help.alteryx.com/sites/default/files/2022-02/OutputTool_0.yxi) and
install this example in Alteryx Designer.

#### Passthrough Tool

An example single-input-single-output tool. This tool takes data from
the input anchor and, without changing it, writes it to the output
anchor. You
can [download](https://help.alteryx.com/sites/default/files/2022-02/PassthroughTool.yxi) and
install this example in Alteryx Designer.
