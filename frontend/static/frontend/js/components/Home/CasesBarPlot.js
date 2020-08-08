import React from 'react';
import {
    MDBCard as Card,
    MDBCardHeader as CardHeader,
    MDBCardBody as CardBody,
} from 'mdbreact';
import Loading from '../Loading';
import { HorizontalBar } from 'react-chartjs-2';
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
        labels: [],
    }

    componentDidMount() {
        fetch(`/api/${this.props.endpoint}`)
            .then(res => res.json())
            .then(res => {
                let { labels, datasets } = res;
                this.setState({
                    labels,
                    data: datasets,
                    loading: false,
                });
            });
    }

    render() {
        let { data, labels } = this.state;

        if (this.state.loading) return <Loading />;
        else return (
            <div className='mb-3 mx-0 px-0'>
                <Card>
                    <CardHeader className='text-left text-uppercase text-muted'>
                        {this.props.cardTitle}
                    </CardHeader>
                    <CardBody className='m-0'>
                        <HorizontalBar
                            data={data}
                            options={{
                                scales: {
                                    xAxes: [{
                                        stacked: true,
                                        scaleLabel: {
                                            display: !!(this.props.xLabel),
                                            labelString: this.props.xLabel,
                                        }
                                    }],
                                    yAxes: [{
                                        type: "category",
                                        labels: labels,
                                        stacked: true,
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
