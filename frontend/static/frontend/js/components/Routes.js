import React, { lazy } from 'react';
import { Route, Switch } from 'react-router-dom';


const Home = lazy(() => import('./Home/Home')),
      Docs = lazy(() => import('./Docs/Docs')),
      Err404 = lazy(() => import('./NotFound'));


const routes = [
    { path: '/docs', name: 'Docs', Component: Docs },
    { path: '/', name: 'Home', Component: Home },
];

export default (
    <Switch>
        {routes.map(({ path, Component }, i) => (
            <Route key={path} exact path={path} component={Component} />
        ))}
        <Route key={404} status={404} component={Err404} />
    </Switch>
);
