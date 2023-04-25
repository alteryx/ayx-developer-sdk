# Test Scaffolding
:::

::: node--info
::: node--info--modified
Last modified: August 01, 2022
:::
:::

::: {.paragraph .paragraph--type--simple-content .paragraph--view-mode--default}
::: {.clearfix .text-formatted .field .field--name--field-information .field--type--text-long .field--label--hidden}
## What is pytest? {#what-is-pytest .index-item}

Pytest is a [unit testing
framework](../../external.html?link=https://docs.pytest.org/en/7.1.x/ "unit testing framework"){rel="noopener"
target="_blank"} intended to test the Python code you write.

## Install pytest {#install-pytest .index-item}

To install pytest run this command:

`pip install pytest`

You can install a specific pytest version, for example:

`pip install pytest==5.4.1`

We use version 5.4.1 internally, but these tests should run on later
versions of pytest as well.

## Run pytest {#run-pytest .index-item}

Once you install pytest, you should be able to run your tests from the
workspace root via:

`ayx_plugin_cli test`

or

`pytest .\backend`

Pytest looks through this directory for any Python functions that fit
the pattern `test_*`.

### IDE Integration

One nice thing about pytest is that it works well with all widely used
integrated development environments (IDEs), like PyCharm, and VSCode.
You can discover and run tests from these IDEs with the touch of a
button, and get test results delivered in a nice breakdown. However,
there might be some setup involved to get this integration working.

### PyCharm

Go to **File** \> **Settings** \> **Tools** \> **Integrated Python
Tools**, and make sure that under **Testing**, the default test runner
is set to pytest.

Once this is set, PyCharm takes a moment to index your files and
discover the tests. When PyCharm is finished, a green run button
displays to the left of each test you can run. To run all of the tests
in a file, select and hold (or right-click) on the file and select the
`Run pytest in <filename>` option.

### VSCode

When you open VSCode, you should see a **Testing** tab on the leftmost
side. Select this tab, and it should indicate that no tests have been
found yet and that you can configure a test framework.
Select **Configure Python Tests**, and then select `pytest`. Use the
`backend` folder as the directory that contains the tests. The
discovered tests should populate in that window.

### Notes

If test discovery fails, and the error message given is an import error,
this could be due to an environment issue. Check the bottom-right corner
of the IDE to make sure it\'s set to the conda environment where your
`ayx_python_sdk` and `ayx_plugin_cli` are installed.

You can set breakpoints in both IDEs in roughly the same way. Hover over
the line numbers on the left to see a little red dot appear. Select and
run the test in debug mode, and you\'ll be able to stop execution at
that point and examine the values of local variables.

## Generate Test {#generate-test .index-item}

Any plugins generated with ayx_plugin_cli version 1.0.3+ should also
come with unit test scaffolds. However, you can generate these scaffolds
for early v2 plugins as well with the new
`ayx_plugin_cli generate-tests` command.

### Command Usage

To generate tests for all tools in a workspace, run this command at the
workspace root:

`ayx_plugin_cli generate-tests`

To specify which tools you want to generate tests for, use:

`ayx_plugin_cli generate-tests --tool-name Tool1 --tool-name Tool2`

Note that you can only generate tools this way if the tool already
exists in your `ayx_workspace.json`, using the same name as the tool's
`tool_class_name` attribute.

Also note that if you generate tests for tools that already exist, the
tests need to be updated to reflect your plugin code.

## Write Tests {#write-tests .index-item}

To discover tests (by default), pytest searches for files that match the
patterns `test_*.py` or `*_test.py`. Any functions that match the
pattern `test_*()` are marked as tests within these files.

Use `assert` statements to check your code\'s values against an expected
outcome, for example:

`assert "value" in ["expected", "value"]`

When a test runs, there are 3 possible outcomes:

-   The test code runs to the end without issue.
-   An unexpected error is raised.
-   The test fails on an assertion check.

The goal of unit testing is to discover these test failures ahead of
time, and debug your logic until your output matches the expected
output.

## Interact with the Plugin Service {#interact-with-the-plugin-service .index-item}

SdkToolTestService is a middleware layer that mocks out some of Alteryx
Designer\'s functionality and allows you to test your plugin\'s
callbacks in an isolated environment. By default, we generate a pytest
fixture that wraps and returns an instance of SdkToolTestService. The
class contains several helper methods and attributes to make your
testing experience easier:

### io_stream

This attribute mocks out Designer\'s Messages window---basically, any
strings that are sent over through `provider.io` calls. When you run
your test, you can examine `plugin_service_fixture.io_stream` to see
which messages were captured, and compare them against a list of
expected messages. Note that `io_stream` is a list of strings, prepended
with the `provider.io` call in question. This is roughly the format they
follow:

`"<INFO|WARN|ERROR>:<message>"`

For example, this \`provider.io\` call in the plugin code:

`self.provider.io.info("Test Code")` shows up as `"INFO:Test Code"` in
`io_stream`.

### data_streams

This attribute mocks out the plugin\'s output anchor. In other words,
any data that shows up in a Browse tool placed after the plugin in
Designer, should show up here. In the plugin code, this is any data that
is written to `provider.io.write_to_anchor()`. When you run your test,
you can examine `data_streams` to ensure that the correct output data
was written to the output anchor, and compare the captured record
batches against a list of expected record batches.

For the purpose of simplicity, the completed stream is represented by a
dictionary, typed like this:

`{ "<Output Anchor name>": [pa.RecordBatch] }`

If `provider.io.write_to_anchor` is never called, the `data_streams`
attribute should be an empty dictionary.

### run_on_record_batch

This method runs your plugin\'s on_record_batch method. Pass it an input
anchor and a corresponding record batch, and it should run the method
and capture the I/O and data stream outputs.

### run_on_incoming_connection_complete

This method runs your plugin\'s on_incoming_connection_complete method,
on the specified input anchor, and captures the data and I/O output.

### run_on_complete

This method runs your plugin\'s on_complete method and captures the data
and I/O output.

### Autogenerated Tests

By default, we generate these 4 tests:

-   test_init
-   test_on_record_batch
-   test_on_incoming_connection_complete
-   test_on_complete

However, you can add as many, or as few, as needed. By default, these
run the corresponding SdkToolTestService methods and compare them to the
default output.

One thing to note is that the on_record_batch test is parametrized, and
runs 3 times by default, one for each batch named in the list argument.

These batches are defined in `conftest.py`. Edit, rename, and change
these to suit your testing needs.

## Examples {#examples .index-item}
:::
:::

::: compound-code-block-container
::: {.paragraph .paragraph--type--compound-code-block .paragraph--view-mode--default .accordion responsive-accordion-tabs="tabs" multi-expand="true"}
::: {.accordion-item accordion-item=""}
[Python](#){.accordion-title}

::: {.accordion-content tab-content=""}
` `

::: {.field .field--name--field-code-geshi .field--type--geshifield .field--label--hidden}
::: geshifilter
::: {.python .geshifilter-python style="font-family:monospace;"}
``` {style="font-family: monospace; font-weight: normal; font-style: normal"}
@pytest.mark.parametrize("record_batch", ["small_batch", "medium_batch", "large_batch"])
def test_on_record_batch(plugin_service_fixture, anchor, record_batch, request):
    record_batch = request.getfixturevalue(record_batch)
    plugin_service_fixture.run_on_record_batch(record_batch, anchor)
    #  In this case, since the tool is a simple passthrough, the input data should match the output data, 1-1.
    assert plugin_service_fixture.data_streams["Output"] == [record_batch]
    #  In this case, there are no calls being made to provider.io, so the io_stream for on_record_batch should be empty.
    assert plugin_service_fixture.io_stream == []
```
:::
:::
:::

Copy Code
:::
:::
:::
:::

::: compound-code-block-container
::: {.paragraph .paragraph--type--compound-code-block .paragraph--view-mode--default .accordion responsive-accordion-tabs="tabs" multi-expand="true"}
::: {.accordion-item accordion-item=""}
[Python](#){.accordion-title}

::: {.accordion-content tab-content=""}
` `

::: {.field .field--name--field-code-geshi .field--type--geshifield .field--label--hidden}
::: geshifilter
::: {.python .geshifilter-python style="font-family:monospace;"}
``` {style="font-family: monospace; font-weight: normal; font-style: normal"}
def test_on_incoming_connection_complete(plugin_service_fixture, anchor):
    plugin_service_fixture.run_on_incoming_connection_complete(anchor)
    #  In this case, no data was written to any of the output anchors, so the streams should be empty.
    assert plugin_service_fixture.data_streams == {}
    #  In this case, the only call being made is "Connection connection on Anchor anchor" as an info message.
    assert plugin_service_fixture.io_stream == [f"INFO:Connection {anchor.connection} on Anchor {anchor.name}"]
```
:::
:::
:::

Copy Code
:::
:::
:::
:::

::: compound-code-block-container
::: {.paragraph .paragraph--type--compound-code-block .paragraph--view-mode--default .accordion responsive-accordion-tabs="tabs" multi-expand="true"}
::: {.accordion-item accordion-item=""}
[Python](#){.accordion-title}

::: {.accordion-content tab-content=""}
` `

::: {.field .field--name--field-code-geshi .field--type--geshifield .field--label--hidden}
::: geshifilter
::: {.python .geshifilter-python style="font-family:monospace;"}
``` {style="font-family: monospace; font-weight: normal; font-style: normal"}
def test_on_complete(plugin_service_fixture):
    plugin_service_fixture.run_on_complete()
    #  In this case, no data was written to any of the output anchors, so the streams should be empty.
    assert plugin_service_fixture.data_streams == {}
    #  In this case, the only call being made is "Pass through tool done" as an info message.
    assert plugin_service_fixture.io_stream == ["INFO:Pass through tool done"]
```
:::
:::
:::