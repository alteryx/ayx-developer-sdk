# Copyright (C) 2022 Alteryx, Inc. All rights reserved.
#
# Licensed under the ALTERYX SDK AND API LICENSE AGREEMENT;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.alteryx.com/alteryx-sdk-and-api-license-agreement
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Example optional input anchor tool."""
from typing import TYPE_CHECKING

from ayx_python_sdk.core import PluginV2

import pandas as pd
import pyarrow as pa
from multiprocessing import Process, Queue


import tensorflow as tf
import logging

from tensorflow.keras import layers
from tensorflow.keras import losses
from pathlib import Path

from .keras_custom_objects import custom_standardization


tf.keras.utils.disable_interactive_logging()


if TYPE_CHECKING:
    from ayx_python_sdk.providers.amp_provider.amp_provider_v2 import AMPProviderV2
    from ayx_python_sdk.core.constants import Anchor

logger = logging.getLogger()

    

class TextClassifier(PluginV2):
    """Concrete implementation of an AyxPlugin."""

    def __init__(self, provider: "AMPProviderV2") -> None:
        """Construct a plugin."""
        self.provider = provider
        self.data_url = self.provider.tool_config["datasetConfig"]["datasetTargetDir"]
        self.training_data_dir = self.provider.tool_config["datasetConfig"]["trainingSetDir"]
        self.test_data_dir = self.provider.tool_config["datasetConfig"]["testSetDir"]
        self.input_anchor = self.provider.incoming_anchors["Input"]
        self.info("Plugin initialized.")
        self.model = None
        self.MODE = "PREVIEW"
        self.model_save_loc = self.provider.tool_config["modelConfig"]["modelName"]
        self.exported_model = f"{self.model_save_loc}-exported"
        self.train_dir = self.provider.tool_config["datasetConfig"]["trainingSetDir"]
        self.test_dir = self.provider.tool_config["datasetConfig"]["testSetDir"]
        self.val_dir = self.train_dir
        if self.MODE == "PREDICT":
            self.model = tf.keras.saving.load_model(self.provider.tool_config["modelConfig"]["modelName"], custom_objects={'custom_standardization': custom_standardization})


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

    def on_incoming_connection_complete(self, anchor: "Anchor") -> None:  # type: ignore
        """
        Call when an incoming connection is done sending data including when no data is sent on an optional input anchor.

        This method IS NOT called during update-only mode.

        Parameters
        ----------
        anchor
            NamedTuple containing anchor.name and anchor.connection.
        """
        self.info(
            f"Received complete update from {anchor.name}:{anchor.connection}."
        )

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
            self.provider.io.info("Loaded model, predicting...")
            
            try:
                results = model.predict(batch['Beep'].to_pylist())
                self.provider.io.info(str(results))
            except Exception as e:
                self.provider.io.error(f"ERR during predict")
                raise e
                
            df = pd.DataFrame({"Results": [float(n[0]) for n in results]})
            batch_to_send = pa.RecordBatch.from_pandas(df=df, preserve_index=False)
            self.provider.write_to_anchor("Output", batch_to_send)
            self.info("TextClassifier tool done.")

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
            self.info(str(e))
            self.provider.io.error(f"An invalid key or value was provided: {str(e)}")
        return (
                root_url,
                max_features,
                seq_length,
                embedding_dim,
                model_save_loc,
                epochs
            )

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

        self.info("Completed data prep...")
        try:
            tf.data.Dataset.save(raw_train_ds, f"{self.data_url}/train")
            tf.data.Dataset.save(raw_test_ds, f"{self.data_url}/test")
            tf.data.Dataset.save(raw_val_ds, f"{self.data_url}/validation")
        except Exception as e:
            logger.error(str(e))

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
                self.info(str(fn_args))
                # TODO: Update this to its own function.
                df = pd.DataFrame({"Results": [0.0, 0.0]})
                batch_to_send = pa.RecordBatch.from_pandas(df=df, preserve_index=False)
                self.provider.write_to_anchor("Output", batch_to_send)
                q = Queue()
                p = Process(target=self.create_and_save_model, args=(q, *fn_args))
                p.start()
                history = q.get()
                p.join()
                history_dict = history.history
                self.info(str(history_dict))
                conf = self.provider.full_config
                self.info(str(conf))
                self.info("Setting new history")

                # Pot, meet kettle. Need another method or opportunity for Additional Execercise section?
                ui_history = {}

                ui_history["trainingLoss"] = history_dict["loss"]
                ui_history["trainingBinaryAccuracy"] = history_dict["binary_accuracy"]
                ui_history["validationLoss"] = history_dict["val_loss"]
                ui_history["validationBinaryAccuracy"] = history_dict["val_binary_accuracy"]
                conf['Configuration']["modelEvaluation"]['history'] = ui_history
                self.info(str(conf))
                self.provider.save_full_config(conf)
            elif self.MODE == 'PREVIEW':
                self.send_preview_data()

        except Exception as e:
            self.provider.io.error(f"Error occuried during creation of model: \n {e}")


    def info(self, s: str):
        logger.info(s)
        self.provider.io.info(s)
