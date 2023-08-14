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