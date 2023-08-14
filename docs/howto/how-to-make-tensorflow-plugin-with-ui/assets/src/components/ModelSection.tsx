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