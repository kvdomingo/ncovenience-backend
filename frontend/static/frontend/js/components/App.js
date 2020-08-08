import React, { Suspense } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import Navbar from './Navbar';
import Footer from './Footer';
import Loading from './Loading';
import Routes from './Routes';
import './App.css';


export default function App() {
    return (
        <Router>
            <Navbar />
            <Suspense fallback={<Loading />}>
                {Routes}
            </Suspense>
            <Footer />
        </Router>
    );
}
