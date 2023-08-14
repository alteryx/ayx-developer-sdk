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