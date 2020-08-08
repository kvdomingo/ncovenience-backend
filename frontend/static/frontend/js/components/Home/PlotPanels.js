import React from 'react';
import CasesLinePlot from "./CasesLinePlot";
import CasesBarPlot from "./CasesBarPlot";


export default function PlotPanels() {
    return (
        <React.Fragment>
            <CasesLinePlot
                endpoint='time-plot'
                cardTitle='Cumulative daily cases'
                yLabel='cumulative number of cases'
            />
            <CasesLinePlot
                endpoint='delta-plot'
                cardTitle='New daily cases'
                yLabel='new cases'
            />
            <CasesLinePlot
                cardTitle='Worldwide cases'
                endpoint='world-plot'
                yLabel='total number of cases (millions)'
            />
            <CasesBarPlot
                endpoint='age-plot'
                cardTitle='Cases by age group'
                xLabel='cases per 100,000 population'
                yLabel='age group'
            />
            <CasesBarPlot
                endpoint='metro-plot'
                cardTitle='NCR cases'
                xLabel='cases per 100,000 population'
            />
        </React.Fragment>
    );
}