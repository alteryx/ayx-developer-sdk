# Extensibility Best Practices

## Small, Sharp Tools

Tools in the workspace should work together. When developing new tools, make them do one focused thing, really well. Follow the [UNIX philosphy](https://en.wikipedia.org/wiki/Unix_philosophy).

* Write tools that do one thing and do it well.
* Write tools to work together.

At Alteryx, you can also solve this with [Alteryx Starter Kits](https://www.alteryx.com/starter-kit).

## Process Data in the Stream

It's tempting to accumulate data from `on_record_batch` and process it in one go on `on_complete`. It's more performant to process data in the stream (process data as it becomes available versus batch it all together).

:information_source:

Why should we process data as it's streamed?
Typically, when you choose to accumulate record batches, you use a `List` in Python. In Computer Science, you might hear this referred to as an `array`. When you append to a `List`, the insertion is fast, since it inserts at the end. However, if there is no reserved space available, `List` reallocates space on the heap that is large enough, copies all the elements, and then appends the item. This is slow since the heap allocator needs to look for a spot in memory with a large enough contiguous location, then copy, which is linear time `O(n)`. On a large enough dataset, this happens many times until there is no memory left or no contiguous memory location can be found to support the resize of `List`.

## Embrace Apache Arrow

In previous versions of the Python SDK, Pandas was king. However, starting with the 2021.4 release and Python SDK version 2.0, Arrow is now a native format. While you can still achieve to/from Pandas with `to_pandas` and `from_pandas`, it's best to stay within the [Arrow](https://arrow.apache.org/) format whenever possible. [PyArrow](https://arrow.apache.org/docs/python/index.html) gives you access to a lot of helpful documentation on the subject, including a large selection of Compute Functions. Note that you can also convert specific columns if necessary, versus entire batches.

For example:
```python
def my_string_mutator(s : str) -> str:
  return s + '_mutated!'

...

# Avoid copying the entire 'batch'. Only 'MyStringColumn' is copied.
adjusted = pa.array(batch.column('MyStringColumn').to_pandas().apply(adjust_datetime))
batch = pa.Table.from_arrays([adjusted, batch.column('Column1'), batch.column('Column2')...], schema=self.schema)
```

Another way to do this is with an [Arrow](https://arrow.apache.org/) compute function.

## Reading CSV Files

Go to [The Fastest Way to Read a CSV in Pandas](https://pythonspeed.com/articles/pandas-read-csv-fast/).

## Multiprocessing/Threading

You should think carefully before you attempt this, as it introduces complexity. Furthermore, the AMP engine maintains a thread pool of its own—it attempts to keep those threads at maximum utilization.

If you're considering a second process/thread, a better option is to write a new tool and chain it together in the workflow. The AMP engine thread pool scheduler attempts to keep various plugins running as necessary. Furthermore, certain languages are only concurrent, not parallel. If you use Python, CPython is likely in use and has the Global Interpreter Lock (GIL).

If you intend to deploy an "all-in-one" tool, Designer offers [Macro](https://help.alteryx.com/20223/designer/macros) functionality.
