import React, { useEffect, useState } from 'react';
import Helmet from 'react-helmet';
import {
    MDBRow as Row,
    MDBCol as Col,
    MDBContainer as Container,
    MDBTypography as Type,
} from 'mdbreact';
import Loading from "../Loading";
import Map from "./Map";
import CounterPanels from './CounterPanels';
import PlotPanels from './PlotPanels';
import Cookies from 'js-cookie';


export default function Home() {
    const [token, setToken] = useState('');

    useEffect(() => {
        let csrftoken = Cookies.get("csrftoken");
        fetch("/api/get-access-token", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken,
            },
        })
            .then(res => res.json())
            .then(res => setToken(res.mapboxApiToken));
    });

    if (!token) return <Loading />;
    else return (
        <React.Fragment>
            <Helmet>
                <title>Dashboard | NCOVENIENCE</title>
            </Helmet>

            <Row className='row-cols-1 row-cols-md-2'>
                <Col>
                    <Map mapboxApiToken={token} />
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
