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