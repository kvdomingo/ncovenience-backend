import React from 'react';
import {
    MDBCard as Card,
    MDBCardHeader as CardHeader,
    MDBCardBody as CardBody,
} from 'mdbreact';
import HtmlParser from 'react-html-parser';
import Loading from '../Loading';


export default class CounterPanels extends React.Component {
    state = {
        loading: true,
        timeCumulative: '',
    }

    componentDidMount() {
        fetch('/api/time-plot')
            .then(res => res.json())
            .then(timeCumulative => this.setState({ timeCumulative, loading: false }));
    }

    render() {
        if (this.state.loading) return <Loading />;
        else return (
            <div className='mb-3 mx-0 px-0'>
                <Card>
                    <CardHeader className='text-left text-uppercase text-muted'>
                        Cumulative daily cases
                    </CardHeader>
                    <CardBody className='m-0'>
                        {HtmlParser(this.state.timeCumulative.plot)}
                    </CardBody>
                </Card>
            </div>
        );
    }
}
