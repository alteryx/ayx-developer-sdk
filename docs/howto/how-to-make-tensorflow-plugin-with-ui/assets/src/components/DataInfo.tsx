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
