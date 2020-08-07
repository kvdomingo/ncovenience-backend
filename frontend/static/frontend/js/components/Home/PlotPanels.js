import React from 'react';
import {
    MDBCard as Card,
    MDBCardHeader as CardHeader,
    MDBCardBody as CardBody,
} from 'mdbreact';
import Loading from '../Loading';
import moment from "moment";
import { Line } from 'react-chartjs-2';


export default class CounterPanels extends React.Component {
    state = {
        loading: true,
        timeCumulative: [],
    }

    componentDidMount() {
        fetch('/api/time-plot')
            .then(res => res.json())
            .then(res => {
                let dataStyle = {
                        fill: false,
                        pointRadius: 1,
                        pointHoverRadius: 10,
                    };
                res.datasets.forEach((category, i) => {
                    res.datasets[i] = { ...res.datasets[i], ...dataStyle };
                    category.data.forEach((dat, j) => {
                        category.data[j].x = moment(dat.x);
                    });
                });
                this.setState({ timeCumulative: res, loading: false });
            });
    }

    render() {
        let { timeCumulative } = this.state;

        if (this.state.loading) return <Loading />;
        else return (
            <div className='mb-3 mx-0 px-0'>
                <Card>
                    <CardHeader className='text-left text-uppercase text-muted'>
                        Cumulative daily cases
                    </CardHeader>
                    <CardBody className='m-0'>
                        <Line
                            data={timeCumulative}
                            options={{
                                scales: {
                                    xAxes: [{
                                        type: "time",
                                        time: {
                                            unit: "month"
                                        }
                                    }]
                                }
                            }}
                        />
                    </CardBody>
                </Card>
            </div>
        );
    }
}
