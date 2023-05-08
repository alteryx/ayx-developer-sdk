# 1. Create a Basic Text Classifier Nueral Network with Tensorflow

In this guide, we use the [Alteryx Python SDK](https://pypi.org/project/ayx-python-sdk/), [Alteryx UI-SDK](https://github.com/alteryx/dev-harness), and [Alteryx Plugin CLI](https://pypi.org/project/ayx-plugin-cli/) to illustrate how to create, train, and call a Tensorflow Keras Neural Network model in a workflow.
To achieve this, We'll reference Tensorflow's [official tutorial](https://www.tensorflow.org/tutorials/keras/text_classification) and recreate the Basic Text Classifier as a workflow tool!

Upon completing this guide, you will know how to:
- Develop, debug, and troubleshoot using the Python and UI SDKs
- Exchange data between UI and Python SDK processes; during both `UPDATE` and `RUN` modes
- Use metaprogramming, Python SDK, and the UI SDK to create editable configuration and dynamic behaviour between or during workflow runs
- Package and use 3rd party libraries from `npm` and `pypi` in a tool
- Develop "ready to use" keras models from scratch, including models to deploy into production workflows.

- [1. Create a Basic Text Classifier Nueral Network with Tensorflow](#1-create-a-basic-text-classifier-nueral-network-with-tensorflow)
  - [1.1. Prerequisites](#11-prerequisites)
  - [1.2. Overview](#12-overview)
    - [1.2.1. Data](#121-data)
    - [1.2.2. Preview](#122-preview)
    - [1.2.3. TRAIN](#123-train)
    - [1.2.4. Predict](#124-predict)
    - [1.2.5. Create a Plugin](#125-create-a-plugin)
      - [1.2.5.1. ui/TextClassifier/src/index.tsx](#1251-uitextclassifiersrcindextsx)
      - [1.2.5.2. backend/ayx\_plugins/text\_classifier.py](#1252-backendayx_pluginstext_classifierpy)
  - [1.3. Backend: A Naive Tensorflow Text Classifier](#13-backend-a-naive-tensorflow-text-classifier)
    - [1.3.1. Data Mode](#131-data-mode)
      - [Supplemental: Error Handling in the SDK](#supplemental-error-handling-in-the-sdk)
      - [Adding a custom method: `setup_data()`](#adding-a-custom-method-setup_data)
    - [](#)


## 1.1. Prerequisites

While we do our best to provide enough information here for any one with general scripting experience to follow along, the recommended prereqs are provided below for general debugging and troubleshooting knowledge outside of the scope possible here:

* Tensorflow
  * Keras
  * Datasets
* React and Typescript
* General understanding or knowledge of Neural Networks and/or AI/ML algorithms.


## 1.2. Overview

The tool we create will allow a user to generate a Text Classifier NN(Neural Network) from scratch, train it using user defined datasets, evaluate training, and then predict with a "production" version of said model.
As previously mentioned, we'll aim to recreate Tensorflow's Official tutorial model but as a workflow tool. If you run into tensorflow related issues, we recommend you review and cross check code provided in the tutorial.

That in mind, we begin here by creating a "naive" version of our text classifier tool.
That is, a tool without any UI to ensure critical functions are running as intended.
To achieve this, we also mock data and relevant calls to represent what will come from the UI SDK to the python backend, and what the backend will send to the UI SDK via `save_config()` (link to docs here). 
Next, we build our frontend using the UI SDK using its provided `dev-harness`.
Once the back and frontend are complete, we then bundle and deploy using the CLI to do end to end testing.
Finally, we package our dependencies and source for deployment using `create-yxi`.


The tool itself will have 4 "modes": `DATA`, `PREVIEW`, `TRAIN`, `PREDICT`. 

### 1.2.1. Data

When in `DATA` mode, our tool will pull down and prep whatever data the user provides via input fields we'll define.
It will then save the data as a tensorflow dataset, ready for the next mode...

### 1.2.2. Preview

In `PREVIEW` mode, our tool will then use the data provided and any available model information to show a "snapshot" of our data and how it will be fed to the model.
This snapshot will include dynamically populated text classifier information like token translations for our classifier when available.

### 1.2.3. TRAIN

This mode will take the prepped data and call the model's training function on it.
Additionally, the user may use the supplied fields to adjust model parameters, train using an existing model, or create an entirely new one.
Finally, the tool will return a report of the training results to the UI and export a "production" version of the model.

### 1.2.4. Predict

When in `PREDICT` mode, the tool will take text input via the input anchor, then run predictions on them and output those results to its output anchor.


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

### 1.2.5. Create a Plugin
Next, use the `create-ayx-plugin` command and reply to the prompts to generate the our tool template code. For this tool, we want to use the `single-input-single-output`. (may switch to optional*)

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

#### 1.2.5.1. ui/TextClassifier/src/index.tsx
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

#### 1.2.5.2. backend/ayx_plugins/text_classifier.py
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

## 1.3. Backend: A Naive Tensorflow Text Classifier

Here, we use the term naive to describe a tool that assumes perfect input in a known structure. 
Later we will add input fields that accept abitrary values. But we can start with controlled, known, values first to simplify testing.
To further simplify the transition to user populated or abitrary data, we can also create a constants.py file.
Fow now leave it blank, though we'll need it later to create static values for our tests.

We update our tool by "mode" (recall our modes are: `DATA, PREVIEW, TRAIN, PREDICT`).
Considering we need to test building the model in that order anyway, this will make reasoning about our code easier too.


### 1.3.1. Data Mode

For this guide, we'll be using the [imdb moview review dataset](https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz).
This archive is a dataset of movie reviews and their labels for classification.
The labels are binary positive or negative reviews.
The reviews are scrapped from the imdb website and then appropriately labeled.
You may download it now, or during the plugin runtime.
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

where:

`self.MODE = "DATA"`
 is our tool's "run mode" as described earlier in [link to section].

and:

 `self.data_url = self.provider.tool_config["datasetConfig"]["datasetTargetDir"]` 
 and the lines below it are utilizing the `tool_config` dict (link to tool_config in docs) to access data and tool configuration sent by the UI SDK.

You may have already noticed, but `tool_config` will contain the values we said we'd mock before deploying to designer.
Once we have developed our frontend, a user will be able to populate these fields.
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

Two important pieces to note here. If you already understand the concepts below, feel free to skip to the next section!

First, the first A python sdk tool runs as a separate (python) process than designer's own process.
While this provides many benefits, (such as abitrary python tool requirements like tensorflow here) this means *designer* cannot directly access the exceptions python process throws.
The SDK does its best to capture generic errors, but the scope of edge cases is impossibly large. 
Meaning, it is entirely possible to try and catch the "wrong" error type in python, and unintentionally let an exception pass silently.(See python docs for details)
As such, we have seen user cases where tricky exceptions simply slip off the stack uncaught.

A simple example:

```python
# where bar = {"key_0": [0, 1]}
try:
  foo = bar[key_variable][2]
except KeyError as e:
  logger.error(f"An error occured: \n{repr(e)}")
```

This code will catch _an_ error; here a `TypeError`. However, it will _not_ run our `except` we intend. Here, a couple more lines of code will go a long way for the debugging process.
You should understand how the below works, and why, so you can effeciently debug your tool.
If you are not quite sure, check out the [python official docs](https://docs.python.org/3.8/tutorial/errors.html).

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

Whether you knew already, or know now, we recommend the above pattern (Note to reviewers: "when developing for designer" ?) with at least: 
* `try/except` with a general case
* A **log**\* statement logging the exception at the appropriate log level: `logger.INFO`, `logger.WARN`, etc
* A `self.provider.io` **message**\* to notify the user an exception occured, and where to look
  * NOTE: `self.provider.io.error(msg)` will immediately terminate the process! So ensure you log and send any messages _before_ then or in your `finally` block if using one!

\* Note the distinction here as well. A _log_ statement will send your output to `PythonSdk.log` by default. A _message_ (read: `self.provider.io.[info | warn | error]`) will send your output to Designer's IO.

If you have multiple distinct sorts of errors, and/or want to use your own Exception derivatives, we recommend defining [decorators](https://pythonguide.readthedocs.io/en/latest/python/decorator.html) to make your exception handling **short, simple, and reusable across any tool you develop as a python module!**

#### Adding a custom method: `setup_data()`

Now we will add our first custom method to our plugin, `setup_data(self)`.
It may be tempting to write your `DATA` mode code all right where it is called.
**However** we strongly encourage following general coding best practices.
Think first, "how would I do this **in python**?"
Rather than, "how do I do this in the `ayx_python_sdk`?"
When developing with the SDK, we encourage developers to use python to its fullest potential.
Therefore, we place our `DATA` mode code in its own function, `setup_data(self)`.
This naturally helps isolate problem areas in your code, makes debugging much easier, and (like mentioned above) makes even **more** of your code reusable! 

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

We know already `self.provider.tool_config` is simply a python dict.
Note though, we have to call `int` on some values. This is simply because we get all `tool_config` as `string` types from the UI SDK.
So, we need to convert this to their expected types or even serialize more complex data. (that is enough for its own step-by-step guide)

We retrieve and parse these values, and use them in `tf.keras.utils.text_dataset_from_directory(...)`. 
This loads our raw data into a dataset to be used by tensorflow.
Once we've successfully loaded them _as_ a `tf.Dataset`, we `.save(...)` them at distinct locations for our learning setup. This allows us to use our data in a format optimized for tensorflow and it's training/execution.
As previously mentioned, we recommend the [companion piece](https://www.tensorflow.org/tutorials/keras/text_classification) provided by tensorflow for details regarding tensorflows' api.
There are more insights regarding tensorflow specifics there, but it's too much to cover here.

Now that our data can be retrieved and loaded, we will need some way to prepare it for our model and training.

### 1.3.2 `PREVIEW` mode

First, we put in our new `PREVIEW` mode code and functionality.
For a thorough explanation of each line, check the companion piece per usual.
_(NOTE: we will assume the reader is doing this or understands `keras` and `tensorflow` moving forward)_


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

Here we load a model that(in the near future) will contain a `TextVectorization` tensorflow layer at `model.layers[0]` where `translationVal` is a comma separated values of integer token values to be "translated" to their original string representations as mapped by said `model.layers[0]` layer.
In other words:
```python
# to be populated by user on frontend
translationVal = "00, 01, 02, 03, ... 55"
>> translation_tokens
>> [{"token": 00, "translation": "fibanocci"}, ..., {"token": 55: "translation": "sequence"}]
```

For now, we won't have any `translationVal`s, so this won't be relevant until later sections.
Then, we log to `self.info` as defined below:


#### Function: `self.get_token_translation`

```python
def info(self, s: str):
  """Log s, and then send an `info` message to designer containg s"""
  logger.info(s)
  self.provider.io.info(s)
```

While the method itself is fairly straight-forward, it comes with a point of advice: We retained the difference between **logging** and **messaging** for many reasons.
A primary one being that the tool _user_ does not always need, and even less so *want*, to see debugging output.
That considered, do not use the above as a cruch or without consideration; logging is cheap but _messaging_ is expensive!
A good rule of thumb is to keep your `self.provider.io` calls to a minimum, only sending what your USER needs to see.
Whereas you can leverage `logging` more freely, especially when paired with the available debugging flag (NOTE: reference needed here).
Helpers like the above should be used sparingly or you will risk slowing your tool with expensive IO! _(A very important consideration in ML)_


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

Now, that we have data and a way to feed it as input into our model we a ready to move on to the next mode.


### `MODEL` mode

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

While this method may _appear_ intimidating, don't let it scare you off! This is simply the core code of our companion piece, gently refactored to fit into our tool process's runtime and lifecycle.
In this method we:
  * load our dataset `tf.data.Dataset.save` 's sibling
  * create and adapt our `vectorize_layer: tensorflow.keras.layers.TextVectorization` as recommended by tensorflow
  * cache our datasets (now loading data as `Datasets` begins to payoff!)
  * init, compile, evaluate and save our base model to generate our previews
  * save

You may have noticed we use a decorater here too, `staticmethod`. 