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