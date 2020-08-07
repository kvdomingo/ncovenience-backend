import React from 'react';
import Helmet from 'react-helmet';
import {
    MDBRow as Row,
    MDBCol as Col,
    MDBContainer as Container,
    MDBTypography as Type,
} from 'mdbreact';
import Map from "./Map";
import CounterPanels from './CounterPanels';
import PlotPanels from './PlotPanels';


export default function Home() {
    return (
        <React.Fragment>
            <Helmet>
                <title>Dashboard | NCOVENIENCE</title>
            </Helmet>

            <Row className='row-cols-1 row-cols-md-2'>
                <Col>
                    <Map />
                </Col>

                <Col>
                    <Container className='my-4'>
                        <Type tag='h1' variant='display-4' className='my-4 text-left'>
                            Dashboard
                        </Type>
                        <div className='text-center'>
                            <CounterPanels />
                            <PlotPanels />
                        </div>
                    </Container>
                </Col>
            </Row>
        </React.Fragment>
    );
}
