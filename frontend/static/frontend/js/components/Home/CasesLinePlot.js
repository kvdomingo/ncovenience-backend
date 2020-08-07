import React from 'react';
import {
    MDBCard as Card,
    MDBCardHeader as CardHeader,
    MDBCardBody as CardBody,
} from 'mdbreact';
import Loading from '../Loading';
import moment from "moment";
import { Line } from 'react-chartjs-2';
import PropTypes from 'prop-types';


export default class CasesLinePlot extends React.Component {
    static propTypes = {
        endpoint: PropTypes.string.isRequired,
        cardTitle: PropTypes.string.isRequired,
        xLabel: PropTypes.string,
        yLabel: PropTypes.string,
    }

    static defaultProps = {
        xLabel: '',
        yLabel: '',
    }

    state = {
        loading: true,
        data: [],
    }

    componentDidMount() {
        fetch(`/api/${this.props.endpoint}`)
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
                this.setState({ data: res, loading: false });
            });
    }

    render() {
        let { data } = this.state;

        if (this.state.loading) return <Loading />;
        else return (
            <div className='mb-3 mx-0 px-0'>
                <Card>
                    <CardHeader className='text-left text-uppercase text-muted'>
                        {this.props.cardTitle}
                    </CardHeader>
                    <CardBody className='m-0'>
                        <Line
                            data={data}
                            options={{
                                scales: {
                                    xAxes: [{
                                        type: "time",
                                        time: {
                                            unit: "month"
                                        },
                                        scaleLabel: {
                                            display: !!(this.props.xLabel),
                                            labelString: this.props.xLabel,
                                        }
                                    }],
                                    yAxes: [{
                                        scaleLabel: {
                                            display: !!(this.props.yLabel),
                                            labelString: this.props.yLabel,
                                        }
                                    }]
                                },
                            }}
                        />
                    </CardBody>
                </Card>
            </div>
        );
    }
}
