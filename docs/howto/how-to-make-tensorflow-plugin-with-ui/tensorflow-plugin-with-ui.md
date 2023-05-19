# Create a Basic Text Classifier Neural Network with TensorFlow

In this guide, we use the [Alteryx Python SDK](https://pypi.org/project/ayx-python-sdk/), [Alteryx UI-SDK](https://github.com/alteryx/dev-harness), and [Alteryx Plugin CLI](https://pypi.org/project/ayx-plugin-cli/) to illustrate how to create, train, and call a Tensorflow Keras Neural Network model in a workflow.
To achieve this, we reference Tensorflow's [official tutorial](https://www.tensorflow.org/tutorials/keras/text_classification) and recreate the Basic Text Classifier as a workflow tool!

The goal of this guide is to teach you to:
- Develop using Python and UI SDKs
- Exchange data between UI SDK and Python SDK processes during both `UPDATE` and `RUN` modes
- Use metaprogramming, Python SDK, and the UI SDK to create an editable configuration and dynamic behavior between (or during) workflow runs.
- Package and use 3rd party libraries from `npm` and `pypi` in a tool
- Develop "ready to use" Keras models from scratch, including models for deploying into production workflows.

- [Create a Basic Text Classifier Neural Network with TensorFlow](#create-a-basic-text-classifier-neural-network-with-tensorflow)
  - [Prerequisites](#prerequisites)
  - [Overview](#overview)
    - [DATA](#data)
    - [PREVIEW](#preview)
    - [TRAIN](#train)
    - [PREDICT](#predict)
  - [Create a Workspace](#create-a-workspace)
  - [Create a Plugin](#create-a-plugin)
      - [ui/TextClassifier/src/index.tsx](#uitextclassifiersrcindextsx)
      - [backend/ayx\_plugins/text\_classifier.py](#backendayx_pluginstext_classifierpy)
  - [Backend: A Naive Tensorflow Text Classifier](#backend-a-naive-tensorflow-text-classifier)
    - [Data Mode](#data-mode)
      - [Supplemental: Error Handling in the SDK](#supplemental-error-handling-in-the-sdk)
      - [Adding a custom method: `setup_data()`](#adding-a-custom-method-setup_data)
    - [`PREVIEW` mode](#preview-mode)
      - [Function: `send_preview_data`](#function-send_preview_data)
      - [Function: `self.get_token_translation`](#function-selfget_token_translation)
      - [Function: `self.get_token_translation`](#function-selfget_token_translation-1)
    - [`TRAIN` mode](#train-mode)
      - [Function: `create_and_save_model`](#function-create_and_save_model)
      - [Function: `get_model_args()`](#function-get_model_args)
      - [Function (Update): `__init__`](#function-update-__init__)
    - [Function (Update): `on_complete`](#function-update-on_complete)
    - [`PREDICT`](#predict-1)
      - [Function: `on_record_batch`](#function-on_record_batch)
  - [Writing the Frontend: UI SDK](#writing-the-frontend-ui-sdk)
    - [Module: `./index.tsx`](#module-indextsx)
    - [Module: `./src/constants.tsx`](#module-srcconstantstsx)
    - [Module:  `./src/components/*`](#module--srccomponents)
      - [Component(s): `config-inputs.tsx`](#components-config-inputstsx)
      - [Component(s): `DataInfo.tsx`, `DataInputSection.tsx`](#components-datainfotsx-datainputsectiontsx)
        - [`DataInfo.tsx`](#datainfotsx)
        - [DataInputSection](#datainputsection)
      - [Component(s): `model-views.tsx`, `ModelSection`, `TokenTranslation`](#components-model-viewstsx-modelsection-tokentranslation)
        - [`model-views.tsx`](#model-viewstsx)
        - [`TokenTranslation.tsx`](#tokentranslationtsx)
        - [`ModelSection.tsx`](#modelsectiontsx)
      - [Component(s): `./src/components/charting/line-plots.tsx`](#components-srccomponentschartingline-plotstsx)
  - [Testing End to End](#testing-end-to-end)
      - [Figure: Tool GUI](#figure-tool-gui)
  - [Package into a YXI](#package-into-a-yxi)
    - [Python Dependencies](#python-dependencies)
    - [React dependencies](#react-dependencies)
    - [CLI packaging command](#cli-packaging-command)
  - [Install and Run in Designer](#install-and-run-in-designer)
    - [Method 1](#method-1)
    - [Method 2](#method-2)
      - [Figure: `DATA` mode:](#figure-data-mode)
      - [Figure: `PREVIEW` mode:](#figure-preview-mode)
      - [Figure: `TRAIN` mode:](#figure-train-mode)
      - [Figure: `PREDICT` mode:](#figure-predict-mode)
  - [Congratulations!](#congratulations)
    - [Exercises](#exercises)


## Prerequisites

This guide aims to provide enough information anyone with general coding experience to follow along.
We recommend these prerequisites for general debugging and troubleshooting outside of the scope of this guide:

* Tensorflow
  * Keras
  * Datasets
* React and Typescript
* General understanding or knowledge of Neural Networks and AI/ML algorithms.

## Overview

The tool we create allows a user to generate a Text Classifier Neural Network (NN) from scratch, train it with user-defined datasets, evaluate training, and then predict with a "production" version of the model.
As mentioned, we'll aim to recreate Tensorflow's official tutorial model as a workflow tool.
If you run into TensorFlow related issues, we recommend you review and cross-check the code provided in the tutorial.

With that in mind, we create a "naive" version of our text classifier tool--that is, a tool without any UI to go over the Tensorflow code and how to convert it for the provider API.
Next, we use the UI SDK and its provided `dev-haress` to build our front end.
Once the back and front ends are complete, we then bundle and deploy using the CLI to do end-to-end testing.
Finally, use `create-yxi` to package our dependencies and source for deployment.

The tool has 4 "modes": `DATA`, `PREVIEW`, `TRAIN`, and `PREDICT`. 

### DATA

In `DATA` mode, our tool will pull down and preps whatever data the user provides via input fields we define.
It then saves the data as a TensorFlow dataset, ready for the next mode.

### PREVIEW

In `PREVIEW` mode, our tool uses the data provided and any available model information to show a "snapshot" of the data and how it is fed into the model.
This snapshot includes dynamically populated text classifier information like token translations for our classifier, when available.

### TRAIN

The `TRAIN` mode takes the prepped data and calls the model's training function.
Additionally, the user can use the supplied fields to adjust model parameters, train using an existing model, or create an entirely new one.
Finally, the tool returns a training results report to the UI and export a "production" version of the model.

### PREDICT

In `PREDICT` mode, the tool will take text input via the input anchor, then run predictions on the input and outputs the results to its output anchor.


## Create a Workspace

Run this code and respond to the prompts.

```powershell
$ mkdir tensorflow-ui-examples
$ cd ./tensorflow-ui-examples/
tensorflow-ui-examples $ ayx_plugin_cli sdk-workspace-init
Package Name: PythonSdkTensorflowExamples
Tool Category [Python SDK Examples]: Tensorflow Python SDK Examples
Description []: Tools using Tensorflow.
Author []: Shawn Owen
Company []: Alteryx
Backend Language (python): python
[Workspace initialization] started
[Workspace initialization] .  Create configuration directory
// output truncated //
[Generating config files] started
[Generating config files] .  generate_config_files:generate_config_xml
[Generating config files] Generating top level config XML file...
[Generating config files] finished
```
Once the above is complete, we recommend you create your Python environment with `venv` or other supported virtual environment modules.
This venv allows you to develop on your machine while deploying with "prod" requirements. We'll also briefly cover how to do that later in the guide.


## Create a Plugin
Next, use the `create-ayx-plugin` command and reply to the prompts to generate our tool template code. For this tool, we want to use the `single-input-single-output`. (may switch to optional*)

```powershell
tensorflow-ui-examples $ ayx_plugin_cli create-ayx-plugin
Tool Name: TextClassifier
Tool Type (input, multiple-inputs, multiple-outputs, optional, output, single-input-single-output, multi-connection-input-anchor) [optional]:
Description []: Create, train, deploy, and use a Tensorflow based text classifier!
Tool Version [1.0]:
DCM Namespace []:
Creating single-input-single-output plugin: Filter UI Tool
[Create plugin] started
[Create plugin] .  Create plugin
[Create plugin] Installing UI components via npm
[Create plugin] Creating Alteryx Plugin...
// output truncated //
[Generating test files for FilterUITool] finished
```

After the command finishes, you should have template files similar to below at the named locations for your UI and python SDK.

#### ui/TextClassifier/src/index.tsx
```jsx
const App = () => {
  const classes = useStyles();
  const [model, handleUpdateModel] = useContext(UiSdkContext);

  useEffect(() => {
    handleUpdateModel(model)
  }, []);

  return (
    <Box p={4}>
     <Grid container spacing={4} direction="column" alignItems="center">
        <Grid item>
          <Alteryx className={classes.alteryx} />
        </Grid>
        <Grid item>
          <Typography variant="h3">
            To get started, edit src/index.tsx
          </Typography>
        </Grid>
      </Grid>
    </Box>
  )
}

const Tool = () => {
  return (
    <DesignerApi messages={{}}>
      <AyxAppWrapper> 
        <App />
      </AyxAppWrapper>
    </DesignerApi>
  )
}

ReactDOM.render(
  <Tool />,
  document.getElementById('app')
);
```

#### backend/ayx_plugins/text_classifier.py
```python
class TextClassifier(PluginV2):
    """A sample Plugin that passes data from an input connection to an output connection."""

    def __init__(self, provider: AMPProviderV2):
        """Construct the plugin."""
        self.name = "TextClassifier"
        self.provider = provider
        self.provider.io.info(f"{self.name} tool started")

    def on_record_batch(self, batch: "pa.Table", anchor: Anchor) -> None:
        # truncated code

    def on_incoming_connection_complete(self, anchor: Anchor) -> None:
        # truncated code

    def on_complete(self) -> None:
        # truncated code
```

## Backend: A Naive Tensorflow Text Classifier

Here, we use the term naive to describe a tool that assumes perfect input in a known structure. 
Later we will add input fields that accept arbitrary values. But we can start with controlled, known values first to simplify testing.
To further simplify the transition to User populated or arbitrary data, we can also create a constants.py file.
For now, leave it blank. We'll need it later to create static values for our tests.

We update our tool by "mode" (recall our modes are: `DATA, PREVIEW, TRAIN, PREDICT`).
Considering we need to test building the model in that order anyway, this will make reasoning about our code more straightforward.


### Data Mode

For this guide, we'll be using the [imdb movie review dataset](https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz).
This archive is a dataset of movie reviews and their labels for classification.
The labels are binary positive or negative reviews.
The reviews are scrapped from the IMDb website and then appropriately labeled.
You may download it now or during the plugin runtime.
Here we download it and reference it locally.
Note that we get this in `.tar.gz` format, so you need to decompress this before using the data.
Once you decompress, note the location as a constant in the `constants.py` module we created earlier.
Something like this will do:

`DATA_SRC = '/path/to/archive/aclImdb_v1.tar/'`

Next, open up `backend/ayx_plugins/text_classifier.py`. It's finally time to add some functional code!

Update the `__init__` method to the below:

```python
    def __init__(self, provider: "AMPProviderV2") -> None:
        """Construct a plugin."""
        self.provider = provider

        self.MODE = "DATA"

        # The location of the raw data
        self.data_url = self.provider.tool_config["datasetConfig"]["datasetTargetDir"]
        # The location to store training datasets for our model
        self.train_dir = self.provider.tool_config["datasetConfig"]["trainingSetDir"]
        # Test datasets, like the training above.
        self.test_dir = self.provider.tool_config["datasetConfig"]["testSetDir"]
        # We pull validation datasets from the same location as our training here
        self.val_dir = self.train_dir

        self.provider.io.info("Plugin initialized.")
```

Where:

`self.MODE = "DATA"`
 is our tool's "run mode," as described earlier in [link to section].

And:

 `self.data_url = self.provider.tool_config["datasetConfig"]["datasetTargetDir"]` 

 And the lines below it utilize the `tool_config` dict (link to tool_config in docs) to access data and tool configuration sent by the UI SDK.

You may have already noticed, but `tool_config` will contain the values we said we'd mock before deploying to Designer.
Once we have developed our frontend, a user can populate these fields.
Until then, you can safely use constants for testing. (better phrasing?)

Next, add the following to the `on_complete` method:

```python
try:
  if self.MODE == 'DATA':
    self.setup_data()
except Exception as e:
  logger = logger.error(f"{self.on_complete}: repr(e)")
  self.provider.io.error(f"{self.on_complete}: an error occuried, please see PythonSDK.log for details!")
```
#### Supplemental: Error Handling in the SDK

There are two crucial pieces to note here. If you already understand the concepts below, feel free to skip to the next section!

First, the first Python sdk tool runs as a separate (python) process from Designer's process.
While this provides many benefits (such as arbitrary Python tool requirements like TensorFlow here), this means *designer* cannot directly access the exceptions the Python process throws.
The SDK does its best to capture generic errors, but the scope of edge cases is impossibly large. 
It is possible to try and catch the "wrong" error type in Python and unintentionally let an exception pass silently. (See Python docs for details)
As such, we have seen user cases where tricky exceptions slip off the stack uncaught.

A simple example:

```python
# where bar = {"key_0": [0, 1]}
try:
  foo = bar[key_variable][2]
except KeyError as e:
  logger.error(f"An error occured: \n{repr(e)}")
```

This code will catch _an_ error; here, a `TypeError`. However, it will _not_ run our `except` we intend. Here, a couple more lines of code will go a long way for debugging.
Your understanding of how the below items function would be best so you can efficiently debug your tool.
If unsure, check out the [official Python docs](https://docs.python.org/3.8/tutorial/errors.html).

```python
except KeyError as e:
  # Key error specific handling
  logger.error(f"Key {EXPECTED_KEY} was not present: \n {repr(e)}")
except Exception as e:
  # Other exception handling
  self.provider.io.warning(f"Unknown Error occured, see {LOG_PATH}/{PythonSDK.log} for details!")
    logger.error(f"Key {EXPECTED_KEY} was not present: \n {repr(e)}")
else:
  # Code that runs when there are no exceptions
  logger.error(f"Key {EXPECTED_KEY} was not present: \n {repr(e)}")
finally:
  # Code that will always run.
  logger.error(f"Key {EXPECTED_KEY} was not present: \n {repr(e)}")
```

Whether you know already or know now, we recommend the above pattern (Note to reviewers: "when developing for designer" ?) with at least: 
* `try/except` with a general case
* A **log**\* statement logging the exception at the appropriate log level: `logger.INFO`, `logger.WARN`, etc
* A `self.provider.io` **message**\* to notify the User an exception occurred and where to look
  * NOTE: `self.provider.io.error(msg)` will immediately terminate the process! So ensure you log in and send any messages _before_ then or in your `finally` block if using one!

\* Note the distinction here as well. A _log_ statement will automatically send your output to `PythonSdk.log`. A _message_ (read: `self.provider.io.[info | warn | error]`) will send your data output to Designer's IO.

If you have multiple distinct sorts of errors or want to use your Exception derivatives, we recommend defining [decorators](https://pythonguide.readthedocs.io/en/latest/python/decorator.html) to make your exception handling **short, simple, and reusable across any tool you develop as a python module!**

#### Adding a custom method: `setup_data()`

Now we will add our first custom method to our plugin, `setup_data(self)`.
It may be tempting to write your `DATA` mode code exactly where it will execute.
**However** we strongly encourage following general coding best practices.
Think, "How would I do this **in Python**?"
Rather than, "How do I do this in the `ayx_python_sdk`?"
When developing with the SDK, we encourage developers to use Python to its fullest potential.
Therefore, we place our `DATA` mode code in its function, `setup_data(self)`.
Separating your steps into functions naturally helps isolate problem areas in your code, makes debugging much easier, and (like mentioned above) makes even **more** of your code reusable! 

```python
  def setup_data(self):
    train_dir = self.provider.tool_config["datasetConfig"]["trainingSetDir"]
    test_dir = self.provider.tool_config["datasetConfig"]["testSetDir"]

    seed = int(self.provider.tool_config["datasetConfig"]["seed"])
    batch_size = int(self.provider.tool_config["datasetConfig"]["batchSize"])

    if Path(train_dir).exists():
      raw_train_ds = tf.keras.utils.text_dataset_from_directory(
        train_dir, 
        batch_size=batch_size, 
        validation_split=0.2, 
        subset='training', 
        seed=seed)
      raw_test_ds = tf.keras.utils.text_dataset_from_directory(
        test_dir,
        batch_size=batch_size)
      raw_val_ds = tf.keras.utils.text_dataset_from_directory(
        train_dir,
        batch_size=batch_size, 
        validation_split=0.2, 
        subset='validation', 
        seed=seed)
      
      try:
        tf.data.Dataset.save(raw_train_ds, f"{self.data_url}/train")
        tf.data.Dataset.save(raw_test_ds, f"{self.data_url}/test")
        tf.data.Dataset.save(raw_val_ds, f"{self.data_url}/validation")
        self.info("Completed data prep...")
      except Exception as e:
        logger.error(repr(e))
```
We know already `self.provider.tool_config` is simply a Python dict.
Note, though, we have to call `int` on some values. We do this simply because we get all `tool_config` as `string` types from the UI SDK.
So, we need to convert this to their expected types or even serialize more complex data. (that is enough for its step-by-step guide)

We retrieve and parse these values and use them in `tf.keras.utils.text_dataset_from_directory(...)`. 
This function loads our raw data into a dataset to be used by TensorFlow.
Once we've successfully loaded them _as_ a `tf.Dataset`, we `.save(...)` them at distinct locations for our learning setup. Saving them as datasets allows us to use our data in a format optimized for TensorFlow and its training/execution.
As previously mentioned, we recommend the [companion piece](https://www.tensorflow.org/tutorials/keras/text_classification) provided by TensorFlow for details regarding TensorFlow's API.
There are more insights regarding TensorFlow specifics, but it's too much to cover here.

Now that our data can be retrieved and loaded, we will need some way to prepare it for our model and training.

### `PREVIEW` mode

First, we put in our new `PREVIEW` mode code and functionality.
To better understand TensorFlow usage, please recheck the companion piece for a more detailed explanation of each line.
_(NOTE: we will assume the reader is doing this or understands `keras` and `tensorflow` moving forward)_
****

#### Function: `send_preview_data`

```python
def send_preview_data(self):
  raw_train_ds = tf.data.Dataset.load(f"{self.data_url}/train")
  conf = self.provider.full_config
  # format for table values
  samples = []
  text_batch, label_batch = [n for n in raw_train_ds.take(1)][0]
  samples = {
    'textBatch': text_batch.numpy()[:2],
    'labelBatch': label_batch.numpy()[:2]
  }
  conf['Configuration']['datasetInfo']['rawTrainSample'] = samples

  translation_val = conf['Configuration']['textVectorizationConfig']['translationRequest']['token']
  if translation_val:
    conf['Configuration']['textVectorizationConfig']['tokenChips'] = self.get_token_translation(translation_val)
    self.info(f"Received value for translation: {str(translation_val)}")

    self.provider.save_full_config(conf)
```

In brief, we load our `tf.data.Dataset` as defined previously in our `DATA` mode. Then, make some sample formats to send to our UI, or "frontend".
Note it also calls two(2) other utility functions called...

#### Function: `self.get_token_translation`

```python

# NOTE TO READER: we will not have a model until the next "MODE", but mentally note the code explanation here

def get_token_translation(self, translationVal):
  model = tf.keras.saving.load_model(f'{self.provider.tool_config["modelConfig"]["modelName"]}-exported', custom_objects={'custom_standardization': custom_standardization})

  try:
    vect_layer = model.layers[0]
    translation_tokens = [token.strip(" ") for token in translationVal.split(",")]
    vect_vocab = vect_layer.get_vocabulary()
    translations = [{"token": int(token), "translation": vect_vocab[int(token)]} for token in translation_tokens]
  
    self.info(str(translations))
    return translations
  except Exception as e:
    logger.error(f"get_token_translation: Error occured \n {repr(e)}")
    self.provider.io.error("An error occured during token translation :( . Please see PythonSdk log for details")
```

`model = tf.keras.saving.load_model(f'{self.provider.tool_config["modelConfig"]["modelName"]}-exported', custom_objects={'custom_standardization': custom_standardization})`

Here we load a model that(soon) will contain a `TextVectorization` TensorFlow layer at `model.layers[0]` where `translational` is a comma-separated value of integer token values to be "translated" to their original string representations as mapped by said `model.layers[0]` layer.


For now, we won't have any `translationVal`s, so this won't be relevant until later sections.
Then, we log in to `self.info` as defined below:

#### Function: `self.get_token_translation`

```python
def info(self, s: str):
  """Log s, and then send an `info` message to designer containg s"""
  logger.info(s)
  self.provider.io.info(s)
```

While the method is relatively straightforward, it includes(spellcheck) a notable point: there is a distinct difference between **logging** and **messaging**.
We chose this for many reasons, a large one being that the tool _User_ rarely needs, and even less so *wants*, to see the debugging output.
Do not use the above as a crunch or without consideration; logging is cheap, but _messaging_ is expensive!
A good rule of thumb is to keep your `self.provider.io` calls to a minimum, only sending what your USER needs to see.
You can leverage `logging` more freely, especially when paired with the available debugging flag (NOTE: reference needed here).
Use sparingly, or you will risk slowing your tool with expensive IO! _(A very important consideration in ML)_

Finally, update `on_complete` to call our `send_preview_data()` function:

```python
self.provider = provider
# ...
self.info("Plugin initialized.")
if self.MODE == 'DATA':
  # ...
elif self.MODE == 'PREVIEW':
  self.send_preview_data()
```

Now, that we have data and a way to feed it as input into our model we are ready to move on to the next mode.

### `TRAIN` mode

Now so far, we've:
* Created custom methods to support TensorFlow API calls
* Added `DATA` mode, a way for a user to input and load a data source as a dataset
* Added `PREVIEW` mode, a way for a user to request preview data from the backend for feedback during data prepping
* Mocked out (actual tests needed) our frontend UI object and tested to verify functionality
  
In our third mode, `MODEL`, a user(NOTE: change to this phrasing in earlier paragraphs?) will input:

* Where to store their generated and trained text classifier NN
* What to name the model
* Various tunable model training parameters
* a TextVectorization option

Then, we will collect the reporting data TensorFlow provides for training and send it to the UI SDK (frontend) for the User to see dynamically generated visual feedback and data from the training session(s).


#### Function: `create_and_save_model`

```python
    @staticmethod
    def create_and_save_model(mp_queue, root_url, max_features, seq_length, embedding_dim, model_save_loc, epochs):

        try:
            raw_train_ds = tf.data.Dataset.load(f"{root_url}/train")
            raw_test_ds = tf.data.Dataset.load(f"{root_url}/test")
            raw_val_ds = tf.data.Dataset.load(f"{root_url}/validation")
        except Exception as e:
            logger.error(str(e))
            raise e
        logger.info("Loaded dataset, starting layer creation")
        try:
        
            vectorize_layer = layers.TextVectorization(
                standardize=custom_standardization,
                max_tokens=max_features,
                output_mode='int',
                output_sequence_length=seq_length)       
        # Make a text-only dataset (without labels), then call adapt
            train_text = raw_train_ds.map(lambda x, y: x)
            vectorize_layer.adapt(train_text)
        except Exception as e:
            logger.error(f"Error while attempting to create vectorize layer: \n {str(e)}")
            raise e
        logger.info("Vectorization Layer complete...")
        try:
            def vectorize_text(text, label):
                text = tf.expand_dims(text, -1)
                return vectorize_layer(text), label

            train_ds = raw_train_ds.map(vectorize_text)
            val_ds = raw_val_ds.map(vectorize_text)
            test_ds = raw_test_ds.map(vectorize_text)
            logger.info("Dataset mapped to text")
            AUTOTUNE = tf.data.AUTOTUNE
            train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
            test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)           
            val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
            logger.info("Dataset cached")
            model = tf.keras.Sequential([
                layers.Embedding(max_features + 1, embedding_dim),
                layers.Dropout(0.2),
                layers.GlobalAveragePooling1D(),
                layers.Dropout(0.2),
                layers.Dense(1)])
            model.compile(loss=losses.BinaryCrossentropy(from_logits=True),
                optimizer='adam',
                metrics=tf.metrics.BinaryAccuracy(threshold=0.0))
            logger.info("beginning training...")
            history = model.fit(train_ds, validation_data=val_ds,
                    epochs=epochs)
            mp_queue.put(history)
            logger.info("Saving...")
            model.save(model_save_loc, save_format='tf', overwrite=True)
        except Exception as e:
            logger.error(f"In precompile {e}")

        try:
            logger.info(f"Training complete!")
            export_model = tf.keras.Sequential([
                vectorize_layer,
                model,
                layers.Activation('sigmoid')
                ])
            logger.info(f"Compiling new model...")
            export_model.compile(
                loss=losses.BinaryCrossentropy(from_logits=False), optimizer="adam", metrics=['accuracy']
            )
            loss, accuracy = model.evaluate(test_ds)
            logger.info(f"Evaluation Results: \n {str(loss)} \n {str(accuracy)}")
            export_model.save(f"{model_save_loc}-exported", save_format="tf", overwrite=True)
        except Exception as e:
            logger.error(f"ERR in TRAIING \n {e}")
            raise e
```

While this method may be intimidating, don't let it scare you! It is simply the core code of our companion piece, gently refactored to fit into our tool's (and the PythonSdk's) runtime and lifecycle.

In this method we:
  * load our dataset `tf.data.Dataset.save's sibling
  * create and adapt our `vectorize_layer: tensorflow.keras.layers.TextVectorization` as recommended by TensorFlow
  * cache our datasets (now loading data as `Datasets` begins to pay off!)
  * init, compile, evaluate, and save our base model.]
  * generate  data for our previews

You may have noticed we use a decorator here as well `static method`.
We do this to allow us to call this using `Multiprocessing`  to train our model without blocking our Python sdk service process. We also add in a multiprocessing queue to quickly retrieve the results and send them to the front end before ending.
Lastly, note that we catch a generalized exception and explicitly raise it for this method. Doing that allows us to throw in a controlled way such that the Designer can report but log it _before_ the process terminates, as we discussed early on in this section of the guide.

As you might have noticed, we currently have a non-trivial amount of arguments.
Since we collect these via IPC (**Read:** InterProcess Communication: N processes running separately; think to Excel and tablue with a linked spreadsheet.), these will also be more difficult to keep in sync.
As such, we want a function to extract these that we can wrap in a try/catch block to explicitly capture and report `KeyErrors` or similarly common exceptions in this context.


#### Function: `get_model_args()`

```python
def get_model_args(self):
  try:
    root_url = self.data_url
    max_features = int(self.provider.tool_config["trainingConfig"]["maxFeatures"])
    seq_length = int(self.provider.tool_config["textVectorizationConfig"]["sequenceLength"])
    # Make a text-only dataset (without labels), then call adapt
    embedding_dim = int(self.provider.tool_config["modelConfig"]["embeddingDim"])
    model_save_loc = self.provider.tool_config["modelConfig"]["modelName"]
    epochs = int(self.provider.tool_config["trainingConfig"]["epochs"])
  except Exception as e:
    self.info(str(e)) # Editing(E)-NOTE: warn method?
    self.provider.io.error(f"An invalid key or value was provided: {str(e)}")
  return (
    root_url,
    max_features,
    seq_length,
    embedding_dim,
    model_save_loc,
    epochs
  )
```

The method above should be pretty straightforward now; good ol' dictionary access. (E-Note: Idiom safe?)
Otherwise, carefully note what we do and do not cast.
Consider why this may be relative to the subsequent code updates in `init` and `on_complete`.

#### Function (Update): `__init__`

```python
    def __init__(self, provider: "AMPProviderV2") -> None:
        """Construct a plugin."""
        # snip... 
        self.model_save_loc = self.provider.tool_config["modelConfig"]["modelName"]
        self.exported_model = f"{self.model_save_loc}-exported"

        self.provider.io.info("Plugin initialized.")
```

### Function (Update): `on_complete`

```python
    def on_complete(self) -> None:
        """
        Clean up any plugin resources, or push records for an input tool.

        This method gets called when all other plugin processing is complete.
In this method, a Plugin designer should perform any cleanup for their plugin.
        However, if the plugin is an input-type tool (it has no incoming connections),
        processing (record generation) should occur here.

        Note: A tool with an optional input anchor and no incoming connections should
        also write any records to output anchors here.
        """
        try:
            if self.MODE == 'DATA':
                self.setup_data()
            elif self.MODE == 'TRAIN':
                fn_args = self.get_model_args()
                # TODO: Update this to its own function.
                # NOTE: Need to remove test data pushes
                df = pd.DataFrame({"Results": [0.0, 0.0]})
                batch_to_send = pa.RecordBatch.from_pandas(df=df, preserve_index=False)
                self.provider.write_to_anchor("Output", batch_to_send)
                q = Queue()
                p = Process(target=self.create_and_save_model, args=(q, *fn_args))
                p.start()
                history = q.get()
                p.join()
                history_dict = history.history
                conf = self.provider.full_config
                self.info("Setting new history")

                # Pot, meet kettle. Need another method or opportunity for Additional Execercise section?
                ui_history = {}

                ui_history["trainingLoss"] = history_dict["loss"]
                ui_history["trainingBinaryAccuracy"] = history_dict["binary_accuracy"]
                ui_history["validationLoss"] = history_dict["val_loss"]
                ui_history["validationBinaryAccuracy"] = history_dict["val_binary_accuracy"]
                conf['Configuration']["modelEvaluation"]['history'] = ui_history
                self.provider.save_full_config(conf)
            elif self.MODE == 'EVAL':
                model = tf.keras.saving.load_model(self.provider.tool_config["modelConfig"]["modelName"], custom_objects={'custom_standardization': custom_standardization})
            elif self.MODE == 'PREVIEW':
                self.send_preview_data()
```


The majority of the above speaks for itself at this point in the guide.
Our most notable (conceptual) addition is likely the `MultiProcessing` section:  

```python
q = Queue()
p = Process(target=self.create_and_save_model, args=(q, *fn_args))
p.start()
history = q.get()
p.join()
```

Note that this is "just enough" to prevent blocking. An incredible amount of resources are available online and on Python's official documentation. For our purposes, know we're using the `Process(...)` to wrap up our expensive compute task - allowing us to avoid blocking the Python server IO.

Now the backend can generate, train, and deploy/export a new model! All that's left now is our final step, allowing the User to use the "production" model to predict data in a workflow!


### `PREDICT`

In our last mode, we must update our `on_record_batch` function to call `model.predict(...)` on values passed to us in the workflow. In our case, we will eventually use a text input for testing.
**NOTE** However, this could be _any_ sort of record batch, as long as it can connect to our anchor and with the appropriate code updates!
In other words, allow Users to use our "production" version for predictions.

Some examples of why one might do this include:
* a tool developer can ship a trained model that exemplifies expected behavior alongside "starter" training data for new user-generated and trained models.
* A tool developer may ship a "base" model, which the User may then tune and train further in their workflow.
* With additional UI, users may choose how/where/when to deploy models in other workflows or jobs.
* Workflows running on Server may do **any of the above to generate serious, performant, and production-grade models**, which also
* Empowers tool **developers AND users** to create production-grade TensorFlow AI/ML pipelines!

#### Function: `on_record_batch`

```python
    def on_record_batch(self, batch: "pa.Table", anchor: "Anchor") -> None:
        """
        Process the passed record batch.

        The method that gets called whenever the plugin receives a record batch on an input.

        This method IS NOT called during update-only mode.

        Parameters
        ----------
        batch
            A pyarrow Table containing the received batch.
        anchor
            A namedtuple('Anchor', ['name', 'connection']) containing input connection identifiers.
        """
        if self.MODE == "PREDICT":
            model = tf.keras.saving.load_model(f'{self.provider.tool_config["modelConfig"]["modelName"]}-exported', custom_objects={'custom_standardization': custom_standardization})
            self.info("Loaded model, predicting...")
            
            try:
                results = model.predict(batch['Beep'].to_pylist())
            except Exception as e:
                self.provider.io.error(f"ERR during predict")
                raise e
                
            df = pd.DataFrame({"Results": [float(n[0]) for n in results]})
            batch_to_send = pa.RecordBatch.from_pandas(df=df, preserve_index=False)
            self.provider.write_to_anchor("Output", batch_to_send)
            self.info("TextClassifier tool done.")
```
Here, we load our model with `keras. saving.load_model(...)`. Note that we append `-exported' to differentiate our training and "production" models. 
As you develop more serious tools, you can create custom methods to deploy and store model deployment and storage. Here, we note the ability to do so!

Then, we call `model.predict(...)` on our loaded model, take the results, and write them to our output anchor for use in the workflow.

Now, this is all of our backend code! Since our (soon-to-exist) tests are passing, we'll move on to our front end and enable these mocked values to be dynamically set by the User!


## Writing the Frontend: UI SDK

_Please Note: if you are unfamiliar with React and the UI SDK, we recommend the (tbd link)[Getting Started with UI SDK and PythonSDK] guide first or as a supplementary, as you may need to reference the above guide for detailed steps._

As some quick prep work, let's make sure you set up your front end. As of (E-Note: version num of "no UI" option?)], if you did not initialize a UI as described in the guide linked above, you might not have one by default. No problem! Run:
`ayx_plugin_cli generate-ui` (E-Note: Correct command?)
Then you should then have your tool's UI files under `workspace-dir/ui/ToolName`. 
Next, we want to start up the UI SDK's [dev-harness](https://alteryx.github.io/alteryx-ui/).
You should be able to run `npm install` and then `npm start` as expected in a React/node app.
If you hit an issue, we recommend referring to the recommended supplementary or other troubleshooting tips in detail on the `alteryx-ui` documentation.

In addition, the depth of React App optimization and how-tos are deep. 
We keep our usage here functional (in the application and user sense of the word) and will explain less in-depth than our TensorFlow backend - as that is what this guide chooses to focus on.

Update `./ui/TextClassifier/src` to reflect the following, taking care to read any notes provided:

### Module: `./index.tsx`

```jsx
import React, { useContext} from 'react';
import ReactDOM from 'react-dom';
import { AyxAppWrapper, Box, Grid, TextField, 
  Typography, Container } from '@alteryx/ui';
import { Context as UiSdkContext, DesignerApi } from '@alteryx/react-comms';
import DataInputSection from './components/DataInputSection';
import ModelSection from './components/ModelSection';
import _ from "lodash";

const Explorer = () => {
  const [model, handleUpdateModel] = useContext(UiSdkContext);
  // (E-Note: Believe we can import and use our text input component here too)
  const onHandleTextChange = (event, configType, key) => {
    const newModel = _.cloneDeep(model);
    newModel.Configuration[configType][key] = event.target.value;
    handleUpdateModel(newModel);
  };


  return (
    <Box marginTop={4}>
      <DataInputSection  />
    <Container>
          <Typography variant="h1" gutterBottom>
      Text Vectorization
    </Typography>
    <Grid alignItems="flex-end" container spacing={2}>
      <Grid item xs>
        <TextField
          fullWidth
          type="number"
          id="sequence-length"
          label="Sequence Length"
          onChange={(e) => onHandleTextChange(e, 'textVectorizationConfig', 'sequenceLength')}
          value={model.Configuration.textVectorizationConfig.sequenceLength || 250}
        />

      </Grid>
    </Grid>
    </Container>
    <Container>
          <Typography variant="h1" gutterBottom>
      Model and Training Configuration
    </Typography>
    <Grid alignItems="flex-end" container spacing={2}>
    <ModelSection />
    </Grid>
    </Container>

    </Box>
  );
};


const App = () => {
  return (
    <Box marginTop={3}>
      <Container>
        <Grid container spacing={3}>
          <Grid item xs={12}>
          
          </Grid>
          <Grid item xs={12}>
            <Explorer />
          </Grid>
        </Grid>
      </Container>
    </Box>
  )
}

const datasetConfig = {
  dataUrl: "",
  datasetTargetDir: ".",
  batchSize: 32,
  seed: 42,
  shouldCache: true,
  trainingSetDir: "aclImdb/train",
  testSetDir: "aclImdb/test", 
}

const datasetInfo = {
  rawTrainSample: 
    {textBatch: [], labelBatch: []}
  ,
  vectorizedSample: {
    sampleRaw: "placeholder sample",
    sampleVectorized: "09 90 1 1 0 0 12",
  },
  vocabIntValue: 0,
  vocabTranslation: '',
}

const textVectorizationConfig = {
  sequenceLength: 250,
  outputMode: 'int',
  outputModeIndex: 0,
  outputModeAnchorEl: null,
  tokenChips: [],
  translationRequest: {
    token: "",
  }
}

const modelConfig = {
  embeddingDim: 16,
  showSummary: false,
  modelName: "text-classifier-model"
}

const modelEvaluation = {
  loss: 0.0,
  accuracy: 0.0,
  history: {
    trainingLoss: [],
    trainingBinaryAccuracy: [],
    validationLoss: [],
    validationBinaryAccuracy: [],
  }
}

const trainingConfig = {
  epochs: 4,
  maxFeatures: 10000,
}

const Configuration = {
  plotUri: [],
  datasetConfig,
  textVectorizationConfig,
  modelConfig,
  trainingConfig,
  modelEvaluation,
  datasetInfo,
}

const defaultConfig = {
  Configuration,
}

const Tool = () => {
  return (
    <DesignerApi messages={{}} defaultConfig={{...defaultConfig}}>
      <AyxAppWrapper> 
        <App />
      </AyxAppWrapper>
    </DesignerApi>
  )
}

ReactDOM.render(
  <Tool />,
  document.getElementById('app')
);
```
While it has an impressive line count by default, our only non-boilerplate additions are skeleton frames in our return statement and default configuration defined and detailed by the `alteryx-ui` API and docs.

### Module: `./src/constants.tsx`

```tsx
export const DS_CONFIG = 'datasetConfig'
export const MDL_CONFIG = 'modelConfig'
export const EVAL_CONFIG = 'modelEvaluation'
```

Next, we need a directory to store our components. In addition, a subdirectory for our charting component.
You should now have

```txt
|- src/
  |- components/
    |- charting/
  |- index.html
  |- index.tsx
  ...
  |- webpack.prod.js
```

### Module:  `./src/components/*`
We can now add the following to our `components` directory.
**Note**: We are again, but for the _frontend_ SDK, creating **reusable** components we could import or place into other tools we or others develop (_depending on a publisher's license and availability_) using your components and vice-versa!
In other words, when we create our first file below, `config-inputs.tsx`, we are creating a component to sprinkle about different places and avoid copying, pasting, and in turn, propagating stale code causing all sorts of sneaky bugs in the near (or even scarier... **FAR** future!!) future.

#### Component(s): `config-inputs.tsx`

```jsx
import React, { useContext } from 'react';
import { TextField } from '@alteryx/ui';
import { Context as UiSdkContext } from '@alteryx/react-comms';
import _ from 'lodash'


const ConfigTextInput = ({value, configType, vKey, elId, label, inputType="string"}) => {
    const [model, handleUpdateModel] = useContext(UiSdkContext);

    const onHandleTextChange = (event, configType, key) => {
        const newModel = _.cloneDeep(model);
        newModel.Configuration[configType][key] = event.target.value;
        handleUpdateModel(newModel);
    };

    return (<TextField
          fullWidth
          type={inputType}
          id={elId}
          label={label}
          onChange={(e) => onHandleTextChange(e, configType, vKey)}
          value={value}
        />)
    }

export {ConfigTextInput};  
```

**Important Note**: One of the few things we will explicitly call out here for the UI SDK, as it is so critical to developing.
React's state model will _not_ "properly" update nested lists (as seen in our defaultConfig) or objects due to how it tracks changes.
Therefore, we use `lodash` as the `alteryx-ui` docs recommended to ensure our `model` stays up to date without stale or redundant data.
A common symptom of this issue is self-replicating lists, i.e.:

```js
// where model will = {someValue: [1], valueToUpdate: 5}
const [model, handleUpdateModel] = useContext(UiSdkContext);
// Create a shallow copy instead of using `lodash` or other method of deepcopy
a = model;

a.valueToUpdate = 8;
// then use `handleUpdateModel` call
// ... promise resovles and..
>> 'a: {someValue: [1, 1], valueToUpdate: 8}'
```

Overall, this simple reusable component allows text input field values to be stored and updated via a given key and value within our config.
You could add other inputs and fields like `FileInput` in this module.

#### Component(s): `DataInfo.tsx`, `DataInputSection.tsx`

##### `DataInfo.tsx`

```jsx
import React, { useContext } from 'react';
import { Grid, Container, Typography, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@alteryx/ui';
import { Context as UiSdkContext } from '@alteryx/react-comms';
import TokenTranslation from "./TokenTranslation";

const DataTable = ({rows}) => {

  return (
  <TableContainer component={Paper}>
    <Table size="small">
      <TableHead>
        <TableRow>
          <TableCell>Label </TableCell>
          <TableCell align="left">Review</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {rows.map((row, rowNum) => (
          <TableRow key={`row-${rowNum}}`}>
            <TableCell component="th" scope="row">
              {row.label}
            </TableCell>
            <TableCell align="right">{row.text}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  </TableContainer>)
};

const VectorizationPreview = ({sampleRaw, sampleVectorized}) => {
    return (<Grid spacing={1} container>
        <Grid item> {sampleRaw} </Grid>
        <Grid item> {sampleVectorized} </Grid>
    </Grid>)
}

export const DataInfo = () => {
    const [model] = useContext(UiSdkContext)
    const tableRows = model.Configuration.datasetInfo.rawTrainSample.textBatch.map((val, index) => {
        return {text: val, label: model.Configuration.datasetInfo.rawTrainSample.labelBatch[index]}
    })
    let vectorzationSample = model.Configuration.datasetInfo.vectorizedSample
    return (
        <Container>
        <Typography variant="h1"> Data Info </Typography>
        <Grid alignItems="flex-end" container spacing={1}>
            <Grid item> <DataTable rows={tableRows} /> </Grid>
            <Grid item> <VectorizationPreview {...vectorzationSample} /> </Grid>
            <Grid item> <TokenTranslation /></Grid>
        </Grid>
        </Container>)
}
```

A data table that accepts `tableRows` to preview samples of our test data as it feeds into our model. Additionally, some vectorization sampling and token samples, as we've defined them in our backend.

##### DataInputSection

```jsx
import React, {useContext, useState} from "react";

import { ConfigTextInput } from './config-inputs';

import { Container, Grid, Typography } from '@alteryx/ui';
import { DS_CONFIG } from '../constants';

import {Context as UiSdkContext} from "@alteryx/react-comms"
import { DataInfo } from "./DataInfo";

const DataInputSection = () => {
    const [model, _] = useContext(UiSdkContext);
    const {datasetInfo} = model.Configuration.datasetInfo
    let inputItems = [
        {configType:DS_CONFIG, vKey:"datasetTargetDir", elId:"dataset-target-dir", label:"Dataset Src Dir"},
        {configType:DS_CONFIG, vKey:"trainingSetDir", elId:"dataset-train-dir", label:"Dataset Training Directory"},
        {configType:DS_CONFIG, vKey:"testSetDir", elId:"dataset-test-dir", label:"Dataset Test Directory"},
        {configType:DS_CONFIG, vKey:"batchSize", elId:"batch-size", inputType:"number", label:"Batch Size"},
        {configType:DS_CONFIG, vKey:"seed", elId:"seed", inputType:"number", label:"seed"},
    ]

    const configTextInputs = inputItems.map((item) => {
        let val = model.Configuration[item.configType][item.vKey]
        
        return <ConfigTextInput {...item} value={val} />
    })

    return (
    <Container>
        <Typography variant="h1"> Data Input </Typography>
        <Grid alignItems="flex-end" container spacing={2}>
            {configTextInputs.map((field, index) => {
                return (<Grid item key={`ds-conf-grid-${index}`}>
                    {field}
                    </Grid>)
            })}
        </Grid>
            <DataInfo  />
        </Container>
    )
}

export default DataInputSection;
```

We define the attributes and key-value pairs for several config text inputs using our earlier defined `ConfigTextInput`.
Then, we bundle them into a grid to neatly display the inputs. You may have noticed, but note the `key` values and `labels and how they match our `provider.tool_config` values we mocked earlier.
As we've discussed, these will be how the User (s) define their data options.
There will also be similar additions for other values in the coming src.

#### Component(s): `model-views.tsx`, `ModelSection`, `TokenTranslation`


##### `model-views.tsx`

```jsx
import React, {useContext} from "react";

import { ConfigTextInput } from './config-inputs';

import { Container, Grid, Typography, Card, CardContent, CardHeader, useTheme } from '@alteryx/ui';
import { MDL_CONFIG } from '../constants';

import {Context as UiSdkContext} from "@alteryx/react-comms"
import { InteractiveLinePlot } from "./charting/line-plots";

const colors = {
    trainingLoss: "rgba(255, 99, 132, 0.5)",
    trainingBinaryAccuracy: "rgba(255, 99, 132, 0.5)",
    validationLoss: "rgba(255, 99, 132, 0.5)",
    validationBinaryAccuracy: "rgba(255, 99, 132, 0.5)",
}

export const ModelTraining = () => {
    const [model] = useContext(UiSdkContext);

    let inputItems = [
        {configType:MDL_CONFIG, vKey:"embeddingDim", elId:"embedding-dim", label:"Embedding Dimension"},
        {configType:MDL_CONFIG, vKey:"modelName", elId:"model-name", label:"Model Name"},
        {configType:"trainingConfig", vKey:"epochs", elId:"epochs", inputType:"number", label:"Epochs"},
        {configType:"trainingConfig", vKey:"maxFeatures", elId:"max-features", inputType:"number", label:"Max Features"},
    ]

    const configTextInputs = inputItems.map((item, i) => {
        let val = model.Configuration[item.configType][item.vKey]
        
        return <ConfigTextInput {...item} value={val} key={`model-cfg-txt-${i}`} />
    })

    const {history} = model.Configuration.modelEvaluation
    const labels = history.trainingLoss.map((_, epochNum) => epochNum + 1)
    const datasets = Object.entries(history).map(([label, data]) => {
            return {
        label,
        data,
        borderColor: colors[label],
        backgroundColor: colors[label]}
            })
    return (
    <Container>
        <Typography variant="h1">Model Evaluation</Typography>
        <Grid alignItems="flex-end" container spacing={2}>
            {configTextInputs.map((field, index) => {
                return (<Grid item key={`ds-conf-grid-${index}`}>
                    {field}
                    </Grid>)
            })}
        </Grid>
        <Grid container>
            <InteractiveLinePlot plotTitle="Eval Results" 
                labels={labels} datasets={datasets} />
        </Grid>
        </Container>
    )
}

const StatCard = ({title, stat}) => {
        return  (<Card>
            <CardHeader title={title} />
            <CardContent>
              <Typography>
                {stat}
              </Typography>
            </CardContent>
          </Card>)
}

export const ModelEvaluation = () => {
    // Filter out the history states for this view
    const [model] = useContext(UiSdkContext);
    const {loss, accuracy} = model.Configuration.modelEvaluation
    let cards = [
        {title: "loss", stat:loss},
        {title: "accuracy", stat: accuracy},
    ]
    return (
    <Container>
        <Typography variant="h1">Model Evaluation Results</Typography>
        <Grid alignItems="flex-end" container spacing={2}>
            {cards.map((card, keyInc) => {
                return (
                    <Grid item key={`stat-item-${keyInc}`}>
                    <StatCard {...card}  />
                    </Grid>
                )}
            )}
        </Grid>
        </Container>
    )
}
```
##### `TokenTranslation.tsx`


```jsx
import React, { useContext, useState } from 'react';
import { Context as UiSdkContext } from '@alteryx/react-comms';
import { Button, Chip, Container, Divider, Grid, TextField } from '@alteryx/ui';

import _ from 'lodash';


const TokenRequestField = () => {
    const [model, handleUpdateModel] = useContext(UiSdkContext)
    const {token} = model.Configuration.textVectorizationConfig.translationRequest

    const tokenUpdateFn = (inputValue) => {
        const newModel = _.cloneDeep(model);
        newModel.Configuration.textVectorizationConfig.translationRequest.token = inputValue
        handleUpdateModel(newModel)
    }

    return (<Container>
        <TextField
          fullWidth
          id="text-vect-config-field"
          label={"Enter a comma separated list of tokens to translate next PREVIEW run."}
          onChange={(event) => tokenUpdateFn(event.target.value)}
          value={token} />
    </Container>)
}

const TokenDisplay = ()=> {
    const [model, handleUpdateModel] = useContext(UiSdkContext)

    const tokenChips = model.Configuration.textVectorizationConfig.tokenChips.map((chip, num) => {
        return {...chip, key: num}
    })

    const handleDelete = targetChip => () => {
        const newModel = _.cloneDeep(model)
        let {tokenChips} = model.Configuration.textVectorizationConfig
        newModel.Configuration.textVectorizationConfig.tokenChips = tokenChips.filter(chip => {
            return chip.key !== targetChip.key
        })
        handleUpdateModel(newModel)
    }

    return (<Grid container justify="center">
        {
            tokenChips ? tokenChips.map((item, i) => {
                let fullLabel = `${item.token}:${item.translation}`
                return (<Grid item key={i} >
                    <Chip label={fullLabel} 
                    onDelete={handleDelete(fullLabel)} />
                    </Grid>) 
            }) : null
        }
    </Grid >)
}

const TokenTranslation = () => {


    return (
        <Container>
            <Container>
            <TokenRequestField />
            </Container>
            <Divider/>
            <Container>
            <TokenDisplay />
            </Container>
        </Container>
    )
}

export default TokenTranslation;
```

##### `ModelSection.tsx`

```jsx
import React, {useState} from "react";

import PropTypes from 'prop-types';
import { Tabs, Tab, AppBar, Typography, Paper, Container, useTheme } from '@alteryx/ui';

import { ModelEvaluation, ModelTraining } from "./model-views";

function TabContainer({ children, dir }) {
  return (
    <Typography component="div" dir={dir} style={{ padding: 8 * 3 }}>
      {children}
    </Typography>
  );
}

TabContainer.propTypes = {
  children: PropTypes.node.isRequired,
  dir: PropTypes.string
};

TabContainer.defaultProps = { dir: 'ltr' };


const ModelSection = () => {
 
  const theme = useTheme();

  const [selectedTab, setValue] = useState(0);

  const modelTabs = {
    0: <TabContainer dir={theme.direction}><ModelTraining  /></TabContainer>,
    1: <TabContainer dir={theme.direction}><ModelEvaluation /></TabContainer>,
  }
    
  return (
    <Container>
      <Paper>
        <AppBar color="default" elevation={0} position="static">
          <Tabs indicatorColor="primary" onChange={(_, newValue) => {setValue(newValue)}} textColor="primary" value={selectedTab} variant="fullWidth">
            <Tab label="Training & Evaluation" />
            <Tab label="Prediction" />
          </Tabs>
        </AppBar>
        {modelTabs[selectedTab]}
      </Paper>
    </Container>
  );
}

export default ModelSection;
```

#### Component(s): `./src/components/charting/line-plots.tsx`


```jsx
import React, {useState} from "react";

import { AppBar, Container, useTheme } from '@alteryx/ui';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export const InteractiveLinePlot = ({labels, plotTitle, datasets, ...rest}) => {
    const theme = useTheme();
    let options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top' as const,
    },
    title: {
      display: true,
      text: plotTitle,
        },
    },
    };

    const data = {
        labels,
        datasets,
        rest
    }

    return (
    <Container>
        <AppBar color="default" elevation={0} position="static">
            {plotTitle} <br />
            <Line options={options} data={data}  />;
        </AppBar>
        
    </Container>
  );
}
```

## Testing End to End
Now, you should see a GUI that looks like the below (E-Note: will add screencap doing one more fresh build for screens since updates):


#### Figure: Tool GUI

[figure here]


## Package into a YXI

First, we should ensure we have all our dependencies for the front and backend. Then, we run `create-yxi` to package each of these into a deployable using their respective package managers.

### Python Dependencies

Add `tensorflow==2.12.0` to your tool's `requirements-third-party.txt`.

### React dependencies

Run `npm install --save lodash chart.js`

### CLI packaging command

Run the `ayx_plugin_cli create-yxi` command, which bundles all the plugins in the workspace into a `.yxi` archive. It should look something like this:

```powershell
$ create-yxi
[Creating YXI] started
[Creating YXI] -- generate_config_files:generate_config_xml
// output truncated //
[Creating YXI] .  create_yxi:create_yxi
[Creating YXI] finished
```

The resulting `.yxi` archive should exist in your plugin workspace's build/exit directory.

## Install and Run in Designer

### Method 1
After you create a `.yxi,` you can double-click the `.yxi` or drag and drop it into Designer to install it. It then prompts you to install the package in a new dialog box. Which looks something like this:

![YXI Install Dialog](./assets/install-yxi-dialog.jpg)

Once it installs, you can find the plugin under the `Tensorflow Python SDK Examples` tool category.

### Method 2
You can also create the `.yxi` _**and**_ install it all in one step via the `designer-install` command. Choose the install option that matches your Designer install. Typically, this is the `user` install option. 



Once the command finishes, open Designer and find your tool under the `Tensorflow Python SDK Examples` tool category.

Drag it into your workflow. Using the recommended dataset (need a reference list, and include this [E-Note: <-]) at your chosen location, fill in the form similar to below:

[TODO: SS of it. Have testing ones, in case]

**TODO/ E-Note: add a selector to the UI; last second thought - debugging or toggling in the shiv directory sucks, and I don't want that smell in the guide—just a toggle switch on the UI for each mode. I forgot to circle back and add that earlier. Quick lift, like a one**

(once it's in) Use the "MODE" selector to run them in the following order, for reasons described at the beginning of the guide: `DATA` -> `PREVIEW` -> `TRAIN` -> `PREDICT.`

Outputs should resemble the following:

#### Figure: `DATA` mode:

[New SS]

#### Figure: `PREVIEW` mode:

[New SS]

#### Figure: `TRAIN` mode:

[New SS]

#### Figure: `PREDICT` mode:

[New SS]

## Congratulations!

You have successfully created your first Tensorflow Keras NN model, from scratch, in a workflow! If you're up to the challenge, we recommend the following exercises to test your new skills!

### Exercises

1. Create a second plugin for your production model.
   1. Try locally using your production model by referencing it on your hard drive.
   2. Convert the above to use a production model included in the yxi as a standalone deployable. (See the Pythons packaging module for idiomatic ways to include your model!)
2. Add a FileExplorer to our text input fields for more intuitive data source input.
3. Add an option to _continue_ training a model rather than overwriting each time.
4. Convert the Tensorflow companion piece exercises.