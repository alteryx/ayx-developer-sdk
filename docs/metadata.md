Metadata is a set of data used to describe the input or output data of a
Python SDK plugin. Plugins use Python Arrow data types to exchange data
with Alteryx Designer. The metadata is used to map this data during the
conversion to or from the internal Designer data format ([Alteryx
Multi-threaded
Processing](../20223/designer/alteryx-amp-engine.html "Alteryx Multi-threaded Processing"){entity-substitution="canonical"
entity-type="node" entity-uuid="e13022bf-27e2-45b6-ae25-0210fe3706a8"
rel="noopener" target="_blank"} or AMP).

## Metadata Description {#metadata-description .index-item}

-   **name**: This is the same as the column name in a dataset.
-   **type**: The internal AMP Designer type.
-   **size**: The size of the data, in bytes.
-   **scale**: Scale is used only for 1 type:
    `fixeddecimal`{renderer-mark="true"}.
-   **source**: This is a string that describes the origin of the data
    (for example, if data is read from a file in Designer, this is set
    to the file path of this input file).
-   **description**: This is an all-purpose string field.

## Why Use Metadata? {#why-use-metadata .index-item}

It\'s not mandatory to use metadata in Python plugins. The simplest
method is typically to create a Python Arrow schema directly, as the
engine derives the necessary types when sent to Designer. But some
plugins might need to export output data types to Designer at plugin
creation to build the workflow. In this case, metadata has to be sent to
Designer through the `__init__`{renderer-mark="true"} method.

Also, sometimes you might need to fine-tune the data type used by
Designer. Metadata is the only way to be sure to map a precise type of
data to Designer because Python Arrow types might not allow for that.
You might also want to modify fields like source or description to send
some specific information through the Designer pipeline. Input metadata
can also be used by the plugin for any reason, for example, the source
field could be a file path the plugin can use.

## Usage {#usage .index-item}

You can use metadata in different places.

### \_\_init\_\_ Method

This method is called at plugin creation when Designer requests the
output data types from the plugin before the workflow runs. You can send
metadata to Designer at this time.

#### Example

In this example, the data schema is a table with 2 columns of types
`int16` and `string`.

    def __init__(self, provider: AMPProviderV2):
        provider.push_outgoing_metadata("Output", create_schema({
            "volts": {
                "type": FieldType.int16
            },
            "device" {
                "type": FieldType.string
            }
        }))

### on_record_batch Method

This method is called each time Designer sends data through the plugin.
You can extract metadata from the input data for information and modify
output data metadata. However, we don\'t recommend modifying the type,
size, and scale as unexpected results can occur in Designer. You can
modify the source and description.

### on_complete Method

On input plugins, a complete schema created with metadata can be
exported to Designer for a precise data schema.

## Use Cases {#use-cases .index-item}

### Define a Schema at \_\_init\_\_

In this example, we specify type `int16`{renderer-mark="true"} for
column `volts`{renderer-mark="true"} and type
`string`{renderer-mark="true"} for column
`device`{renderer-mark="true"}.

    def __init__(self, provider: AMPProviderV2):
        provider.push_outgoing_metadata("Output", create_schema({
            "volts": {
                "type": FieldType.int16
            },
            "device" {
                "type": FieldType.string
            }
        }))

### Add Optional Information to the Data Flow

In this case, `description`{renderer-mark="true"} metadata is added to
the batch.

    def on_record_batch(self, batch: "pa.Table", anchor: Anchor) - > None:
        batch = set_metadata(batch, {
            "volts": {
                "description": "Define the tension of the current"
            }
        })

        self.provider.write_to_anchor("Output", batch)

### Get Information about the Incoming Data

This example shows how to use the `source`{renderer-mark="true"}
metadata. In this case, the source metadata is a file path, but it can
be anything that describes the address of the source of the data.

    def on_record_batch(self, batch: "pa.Table", anchor: Anchor) - > None:
        meta = get_metadata(batch, "volts")
        filepath = meta["source"]
        with f = open(Path(filepath)):
            content = f.read()
            #...additional operations...
        
        self.provider.write_to_anchor("Output", batch)

## Specifications {#specifications .index-item}

For V2 plugins, metadata is stored in PyArrow tables as a Python
dictionary in each column schema. But Arrow doesn't offer easy methods
to access this metadata.
The `ayx_python_sdk.core.utils`{renderer-mark="true"} module provides
functions to ease this access.

### set_metadata

`set_metadata(table, col_meta={}, schema=None)`

This function updates column metadata from the given PyArrow table with
a dictionary of column metadata or directly with a PyArrow Schema. It
returns the new table with the new metadata. The input table remains
unchanged.

#### Example

This example modifies the metadata of 2 columns,
`volts`{renderer-mark="true"} and `ampere`{renderer-mark="true"}.

    def on_record_batch(self, batch: "pa.Table", anchor: Anchor) - > None:
        batch = set_metadata(batch, {
            "volts": {
                "description": "tension"
            },
            "ampere": {
                "source": "https://something.com"
            }
        })

    self.provider.write_to_anchor("Output", batch)

### get_metadata

`get_metadata(table, col_name)`

Get all columns\' metadata or 1 column's metadata if
`col_name`{renderer-mark="true"} is given, from the input PyArrow table.

-   If `col_name`{renderer-mark="true"} is given, only the dictionary of
    metadata for this column is returned.

-   If `col_name`{renderer-mark="true"} is not given, it returns a
    dictionary of column names and their corresponding metadata
    dictionary.

#### Examples {#examples renderer-start-pos="5203"}

    def on_record_batch(self, batch: "pa.Table", anchor: Anchor) -> None:
        meta_for_column_volts = get_metadata(batch, "volts")

The above example `get_metadata`{renderer-mark="true"} returns the
metadata for 1 column, of the following format (in this example):

    meta_for_column_volts = {
        "type": 3,
        "size": 2,
        "scale": 0,
        "source": "",
        "description": ""
    }

::: note
You can see in the above example that a number represents the type.
Please refer to the Types section below for the mapping between type id
and type names.
:::

This example returns all metadata:

    def on_record_batch(self, batch: "pa.Table", anchor: Anchor) -> None:
        all_meta = get_metadata(batch)

The result dictionary looks like this:

    all_meta = {
        "volts": {
            "type": 3,
            "size": 2,
            "scale": 0,
            "source": "",
            "description": ""
        }
        "device": {
            "type": 9,
            "size": 64,
            "scale": 0,
            "source": "",
            "description": ""
        }
    }

Refer to this sequence diagram for a visual representation of the
metadata lifecycle:

::: {.embedded-entity embed-button="image_embed" entity-embed-display="entity_reference:media_image" entity-type="media" entity-uuid="0b4c16f7-f617-4c30-b6a1-0c2aded335f2" langcode="en"}
![](../sites/default/files/image/2022-12/workflow-metadata-lifecycle.png){width="627"
height="453" loading="lazy" typeof="foaf:Image"}
:::

You can find a more complete example at [Metadata Plugin
Example](metadata-plugin-example.html "Metadata Plugin Example"){entity-substitution="canonical"
entity-type="node" entity-uuid="1ed60ab0-8638-4677-9c9c-f1f56232999c"
rel="noopener" target="_blank"}.

## Types {#types .index-item}

The `ayx_python_sdk.core.field`{renderer-mark="true"} module provides a
definition of the Designer types with the class
`FieldType`{renderer-mark="true"}.

It defines a mapping between type names and a number:

    FieldType.bool = 1
    FieldType.byte = 2
    FieldType.int16 = 3
    FieldType.int32 = 4
    FieldType.int64 = 5
    FieldType.fixeddecimal = 6
    FieldType.float = 7
    FieldType.double = 8
    FieldType.string = 9
    FieldType.wstring = 10
    FieldType.v_string = 11
    FieldType.v_wstring = 12
    FieldType.date = 13
    FieldType.time = 14
    FieldType.datetime = 15
    FieldType.blob = 16
    FieldType.spatialobj = 17

If only the type is specified at schema creation, the other metadata
fields are automatically filled (`"size"`{renderer-mark="true"},
`"scale"`{renderer-mark="true"}, and `"source"`{renderer-mark="true"}).

The maximum size specified by `"size"`{renderer-mark="true"} is set to
the biggest when using string types but you can manually specify a size
for string types. For example, if you set 4 as the size for a string,
all strings in the corresponding column are truncated to 4 characters.

### Special Types

-   The type `FieldType.blob`{renderer-mark="true"} is not supported
    yet.

-   The type `FieldType.spatialobj`{renderer-mark="true"} supports
    spatial objects using the text format WKT. In order to use it,
    `"source"`{renderer-mark="true"} metadata must be
    `"WKT"`{renderer-mark="true"} (it\'s automatically set to it), so
    the source metadata field should not be modified.

-   The type `FieldType.fixeddecimal`{renderer-mark="true"} relies on
    `"size"`{renderer-mark="true"} and `"scale"`{renderer-mark="true"}
    metadata items to specify the size of the integer part
    (`size`{renderer-mark="true"}) and the size of the fractional part
    (`scale`{renderer-mark="true"}).
