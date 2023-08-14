import React, {useState} from "react";

import { AppBar, Container, useTheme } from '@alteryx/ui';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);





export const InteractiveLinePlot = ({labels, plotTitle, datasets, ...rest}) => {
    const theme = useTheme();
    let options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top' as const,
    },
    title: {
      display: true,
      text: plotTitle,
        },
    },
    };

    const data = {
        labels,
        datasets,
        rest
    }

    return (
    <Container>
        <AppBar color="default" elevation={0} position="static">
            {plotTitle} <br />
            <Line options={options} data={data}  />;
        </AppBar>
        
    </Container>
  );
}