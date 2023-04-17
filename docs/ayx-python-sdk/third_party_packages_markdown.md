Python 3rd-party Dependencies
=============================

Adding 3rd-party Packages
-------------------------

In many cases, it is useful to add 3rd-party Python packages that can be
used in your plugin. To do this, add dependencies to the
requirements-thirdparty.txt file in the tool workspace directory.

There are 2 options:

1.  Manually add dependencies. If you use this approach, make sure to
    include all dependencies (including any sub-dependencies).

2\. Use `pip freeze > requirements.txt` to generate a new
requirements.txt file in the workspace. You will need to prune this file
to remove any dependencies that aren\'t explicitly imported or required
by your plugin. Do this before you copy or overwrite the contents to the
`requirements-thirdparty.txt` file

Using 3rd-party Packages in Code
--------------------------------

When you use 3rd-party packages in Python, you typically import these
packages at the top of a file. However, if the packages that you use are
large (like numpy, pandas, scikit-learn, etc.), then these imports can
take a long time.

Since the update-only mode of Alteryx Designer should be as fast as
possible, these import statements can be a bottleneck. Because of this,
instead of putting import statements at the top of a file, you should
include these inline so that they only occur just before they are
needed. See the example below for an Input-type tool that uses pandas to
generate its data (note that pandas is imported in the `on_complete`
method):

``` {.sourceCode .python}
class ExampleInput(Plugin):
    """Concrete implementation of an AyxPlugin."""

    def __init__(self, provider: ProviderBase) -> None:
        """Construct a plugin."""
        self.provider = provider
        self.tool_config = provider.tool_config
        self.config_value = self.tool_config["Value"]
        self.output_anchor = self.provider.get_output_anchor("Output")

        self.output_metadata = Metadata()
        self.output_metadata.add_field("x", FieldType.float)
        self.output_metadata.add_field("y", FieldType.v_wstring, size=100)
        self.output_metadata.add_field("z", FieldType.float)

        self.output_anchor.open(self.output_metadata)

        if float(self.config_value) > 0.5:
            raise WorkflowRuntimeError("Values greater than 0.5 are not allowed.")

        self.provider.io.info("Plugin initialized.")

    def on_incoming_connection_complete(self, anchor: "Anchor") -> None:
        """Initialize the Input Connections of this plugin."""
        raise NotImplementedError("Input tools don't have input connections.")

    def on_record_batch(self, "pa.Table", anchor: "Anchor") -> None:
        """Handle the record batch received through the input connection."""
        raise NotImplementedError("Input tools don't receive batches.")

    def on_complete(self) -> None:
        """Create all records."""
        import pandas as pd
        import pyarrows as pa

        df = pd.DataFrame(
            {
                "x": [1, 2, 3],
                "y": ["hello", "world", "from ayx_plugin_sdk!"],
                "z": [self.config_value, self.config_value, self.config_value],
            }
        )

        table = pa.Table.from_pandas(df)

        self.provider.write_to_anchor(table)
        self.provider.io.info("Completed processing records.")
```
