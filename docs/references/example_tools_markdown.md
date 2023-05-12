Example Tools
=============

A suite of example tools ships with the `ayx_python_sdk` package. You
can use these as templates for new tools.

Example Tool Descriptions
-------------------------

These are the example tools and their descriptions:

1.  **AyxSdkInput**: This is an example *input* tool that generates some
    simple data via the pandas library and outputs it on the output
    anchor. The tool has no input anchors, and 1 output anchor.
2.  **AyxSdkOutput**: This is an example *output* tool. It has 1 input
    anchor and no output anchors. The tool does not do any data
    processing with the input data.
3.  **AyxSdkPassthrough**: This is an example *passthrough* tool. It has
    1 input anchor and 1 output anchor. This tool doesn\'t do any
    processing, it just pushes the same data that was received on the
    input anchor to the output anchor.
4.  **AyxSdkMultipleInputAnchors**: This is a tool that has 2 input
    anchors and 1 output anchor. It enforces that the metadata on each
    anchor must be the same, and it merges the data from each input
    anchor on the output anchor, similar to a Union tool.
5.  **AyxSdkOptionalInputAnchor**: This tool has an optional input
    anchor. This means that the plugin can run with or without a
    connection on the input anchor. If there is a connection on the
    input anchor, the plugin acts as a passthrough tool.
6.  **AyxSdkMultipleOutputAnchors**: This tool has 1 input anchor and 2
    output anchors. Provided that the input connection\'s metadata has
    an integer numeric field called \"Value\", this tool separates the
    records from that connection into odds and evens. NOTE: There is a
    known bug that causes the resulting records to be written to both
    output anchors.
7.  **AyxSdkMultiConnectionsMultiOutputAnchor**: This tool has a single
    input anchor that can receive multiple connections. It maps each of
    these input connections to an output anchor according to the order
    in which the input connections were connected.
