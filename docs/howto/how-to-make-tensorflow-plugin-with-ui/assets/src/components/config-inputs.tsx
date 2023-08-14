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