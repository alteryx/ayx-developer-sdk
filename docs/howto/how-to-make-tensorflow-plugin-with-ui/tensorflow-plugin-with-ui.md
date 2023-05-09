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


### Create a Workspace

Run the following, responding as prompted

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

Once the above is complete, we recommmend you create your python environment with `venv` or other supported virtual environment modules.
This will allow you to iteravely develop locally, while you may still deploy with "prod" requirements. We'll briefly cover how to do that later in the guide as well.


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

You may have already noticed, but `tool_config` will contain the values we said we'd mock befiore deploying to designer.
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

While the method itself is fairly straight-forward, it includes(spellcheck) a notable point: there is a distinct difference between **logging** and **messaging**.
There are many reasons we made this choice, a large one being that the tool _user_ does not always need, and even less so *want*, to see debugging output.
Given that, do not use the above as a cruch or without consideration; logging is cheap but _messaging_ is expensive!
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


### `TRAIN` mode

Now so far we've:
* Created custom methods to support tensorflow API calls
* Added `DATA` mode, a way for a user to input and load a data source as a dataset
* Added `PREVIEW` mode, a way for a user to request preview data from the backend for feedback during data prepping
* Mocked out (actual tests needed) our frontend UI object and tested to verify functionality
  
In our third mode, `MODEL`, a user(NOTE: change to this phrasing in earlier paragraphs?) will input:

* Where to store their generated and trained text classifier NN
* What to name the model
* Various tunable model training parameters
* a TextVectorization option

Then, we will collect the reporting data tensorflow provides for training and send it to the UI SDK (frontend) for the user to see dynamically generated visual feedback and data from the training session(s).



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

While this method may be intimidating, don't let it scare you!
This is simply the core code of our companion piece, gently refactored to fit into our tool's (and the PythonSdk's) runtime and lifecycle.

In this method we:
  * load our dataset `tf.data.Dataset.save` 's sibling
  * create and adapt our `vectorize_layer: tensorflow.keras.layers.TextVectorization` as recommended by tensorflow
  * cache our datasets (now loading data as `Datasets` begins to payoff!)
  * init, compile, evaluate and save our base model to generate our previews
  * save

You may have noticed we use a decorater here too, `staticmethod`.
We do this to allow us to call this with `Multiprocessing`  to train our model without blocking our python sdk service process. We also add in a multiprocessing queue to easily retrieve the results and send it to the frontend before ending.
Lastly for this method, note we catch a generalized exception and explicity raise it. This allows us to throw in a controlled way such that designer can report, but log it _before_ the process terminates as we discussed early on in this section of the guide.

As you might have noticed, we currently have a non-trivial amount of arguments.
Since we collect these via IPC (**Read:** InterProcess Communication: N processes running separately; think excel and tablue with a linked spreadsheet.), these will also be more difficult to keep in synch.
As such, we want a function to extract these that we can wrap in a try/catch block to explicitly catch and report `KeyErrors` or similarly common exceptions in this context.


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

This should be fairly straight-forward by now, good ol' dictionary access. (E-NOTE: Idiom safe?)
Otherwise, carefully note what we do, and do not, cast.
Consider why this may be, relative to the next code updates in `init` and `on_complete`.

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

Note that this is, "just enough" to prevent blocking. There are an incredible amount of resources available online and on python's official documentation. For our purposes, just know we're using the `Process(...)` to wrap our expensive compute task - allowing us to avoid blocking the python server IO.

Now the backend can generate, train, and deploy/export a new model! All that's left now is our final step, allowing the user to use the "production" model to predict on data in a workflow!


### `PREDICT`

In our last mode, we will need to update our `on_record_batch` function to allow us to call `model.predict(...)` on values passed to us in the workflow. In our case, we will eventully use a text input for testing.
**NOTE** however, this could be _any_ sort of record batch, as long as it can connect to our anchor and with the appropriate code updates!
In other words, allow our user to use our "production" version for predictions.

Some examples of why one might do this include:
* a tool developer can ship both a trained model that exemplifies expected behaviour alongside "starter" training data for new user-generated and trained models.
* A tool developer may ship a "base" model. This model may then be tuned and trained further by the user in their workflow.
* With additional UI, users may choose how/where/when to deploy models for use in other workflows or jobs.
* Workflows running on Server may do **any of the above to generate serious, performant, and production-grade models** which also...
* Empowers tool **developers AND users** to create production grade tensorflow AI/ML pipelines!

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

Here, we load our model with `keras.saveing.load_model(...)`. Note we append `-exported' to differentiate our training model and "production" model. 
As you develop more serious tools, you are free to develop your own methods of sensical model deployment and storage. Here, we simply note the ability to do so!

Then, we call `model.predict(...)` on our loaded model, take the results, and write them to our output anchor for use in the workflow.

Now, this is all of our backend! Since our (soon to exist) tests are passing, we'll move on to our frontend and enable these mocked values to be dynamically set by the user!


## Writing the Frontend: UI SDK

_Please Note: if you are not familiar with React and the UI SDK, we recommend the (tbd link)[Getting Started with UI SDK and PythonSDK] guide first, or as a supplementary as you may need to reference the above guide for detailed steps._

As some quick prep work, lets make sure you setup your frontend. As of (E-Note: version num of "no ui" option?)], if you did not intialize a ui as described in the guide linked above you may not have one by default. No problem! Simply run:
`ayx_plugin_cli generate-ui` (E-Note: Correct command?)
Then you should then have your tool's UI files under `workspace-dir/ui/ToolName`. 
Next, we want to start up the UI SDK's [dev-harness](https://alteryx.github.io/alteryx-ui/).
You should be able to simply run `npm install` and then `npm start` as expected in a React/node app.
If you hit an issue, we recommend referring to the recommended supplementary or other troubleshooting tips provided in detail on the `alteryx-ui` documentation.

In addition, the depth of React App optimization and how-tos are deep. 
We keep our usage here functional (in the application and user sense of the word), and will explain less in depth than our tensorflow backend - as that is what this guide is focused on.

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

While it comes with an impressive line count by default, our only non-boilerplate additions are skeleton frames in our return statement and default configuration as defined and detailed by the `alteryx-ui` API and docs.

### Module: `./src/constants.tsx`

```tsx
export const DS_CONFIG = 'datasetConfig'
export const MDL_CONFIG = 'modelConfig'
export const EVAL_CONFIG = 'modelEvaluation'
```

Next we need a directory to store our components. In addition, a subdirectory for our charting component.
You should now have

```
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
**Note**: We are again, but for the _frontend_ SDK, creating **reusable** components we could import or place into other tools we or others develop (_depending on a publishers license and availability_) using your components and vice-versa!
In other words, when we create our first file below, `config-inputs.tsx`, we are creating a component to sprinkle about other places and avoid copying, pasting, and in turn propegating stale code casing all sorts of sneaky bugs in the near (or even scarier... **FAR** future!!) future.

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

**Important Note**: One of the few things we will explicitely call out here for the UI SDK, as it is so critical to developing.
React's state model will _not_ "properly" update nested lists (as seen in our defaultConfig) or objects due to how it tracks changes.
Therefore, we use `lodash` as recommended by the `alteryx-ui` docs to ensure our `model` stays up to date without stale or redundant data.
A common symptom of this issue is self-replicating lists, ie:

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


That said, overall this is a simple reusable component to allow text input fields tracked via a given key and value within our config.
In this module, you could add other inputs and fields like `FileInput`.
