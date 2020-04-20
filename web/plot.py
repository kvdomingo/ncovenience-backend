import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from . import data
from datetime import datetime
from plotly.offline import plot
from django.conf import settings
from pandas.core.computation.ops import UndefinedVariableError


bs4_success = '#00c851'
bs4_warning = '#ffbb33'
bs4_danger = '#ff4444'

def get_plot_over_time():
    time_conf_unique = data.get_confirmed_over_time()
    time_recov_unique = data.get_recovered_over_time()
    time_dead_unique = data.get_deaths_over_time()

    time_conf_keys = time_conf_unique.keys()[2:]
    time_conf_vals = (
        time_conf_unique
            .query("`Country/Region` == 'Philippines'")[time_conf_unique.keys()[2:]]
            .sum()
            .values
    )

    time_recov_keys = time_recov_unique.keys()[2:]
    time_recov_vals = (
        time_recov_unique
            .query("`Country/Region` == 'Philippines'")[time_conf_unique.keys()[2:]]
            .sum()
            .values
    )

    time_dead_keys = time_recov_unique.keys()[2:]
    time_dead_vals = (
        time_dead_unique
            .query("`Country/Region` == 'Philippines'")[time_conf_unique.keys()[2:]]
            .sum()
            .values
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time_conf_keys,
        y=time_conf_vals,
        name='Confirmed',
        marker_color=bs4_warning,
        mode='lines',
    ))
    fig.add_trace(go.Scatter(
        x=time_recov_keys,
        y=time_recov_vals,
        name='Recovered',
        marker_color=bs4_success,
        mode='lines',
    ))
    fig.add_trace(go.Scatter(
        x=time_dead_keys,
        y=time_dead_vals,
        name='Deceased',
        marker_color=bs4_danger,
        mode='lines',
    ))
    fig.update_layout(
        legend={
            'x': 0,
            'y': 1,
        },
        legend_orientation='h',
        margin={
            't': 0,
            'l': 0,
            'r': 0,
            'b': 0,
        },
        yaxis_title='cumulative number of cases',
        annotations=[
            dict(
                x=datetime(2020, 1, 30),
                y=time_conf_vals[time_conf_keys.to_list().index(datetime(2020, 1, 30))],
                xref='x',
                yref='y',
                text=f'First PH case | {datetime(2020, 1, 30).strftime("%d %b")}',
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-100,
            ),
            dict(
                x=datetime(2020, 3, 15),
                y=time_conf_vals[time_conf_keys.to_list().index(datetime(2020, 3, 15))],
                xref='x',
                yref='y',
                text=f'Community Quarantine | {datetime(2020, 3, 15).strftime("%d %b")}',
                showarrow=True,
                arrowhead=7,
                ax=-150,
                ay=-50,
            ),
            dict(
                x=datetime(2020, 3, 17),
                y=time_conf_vals[time_conf_keys.to_list().index(datetime(2020, 3, 17))],
                xref='x',
                yref='y',
                text=f'Enhanced Community Quarantine | {datetime(2020, 3, 17).strftime("%d %b")}',
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-100,
            ),
        ],
    )
    return plot(fig, output_type='div', include_plotlyjs=False)


def get_world_over_time():
    time_conf_unique = data.get_confirmed_over_time()
    time_recov_unique = data.get_recovered_over_time()
    time_dead_unique = data.get_deaths_over_time()

    time_conf_unique = time_conf_unique[time_conf_unique.columns[2:]]
    world_conf = time_conf_unique.sum()

    time_recov_unique = time_recov_unique[time_recov_unique.columns[2:]]
    world_recov = time_recov_unique.sum()

    time_dead_unique = time_dead_unique[time_dead_unique.columns[2:]]
    world_dead = time_dead_unique.sum()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=world_conf.index,
        y=world_conf.values,
        marker_color=bs4_warning,
        name='Confirmed',
    ))
    fig.add_trace(go.Scatter(
        x=world_recov.index,
        y=world_recov.values,
        marker_color=bs4_success,
        name='Recovered',
    ))
    fig.add_trace(go.Scatter(
        x=world_dead.index,
        y=world_dead.values,
        marker_color=bs4_danger,
        name='Deceased',
    ))
    fig.update_layout(
        legend_orientation='h',
        legend={
            'x': 0,
            'y': 1,
        },
        margin={
            't': 0,
            'l': 0,
            'r': 0,
            'b': 0,
        }
    )
    return plot(fig, output_type='div', include_plotlyjs=False)


def get_delta_over_time():
    time_conf_unique = data.get_confirmed_over_time()
    time_recov_unique = data.get_recovered_over_time()
    time_dead_unique = data.get_deaths_over_time()

    ph_time = time_conf_unique.query("`Country/Region` == 'Philippines'")
    ph_time = ph_time[ph_time.columns[4:]]
    delta_conf = [0, *np.diff(ph_time.values.squeeze())]
    conf_time = ph_time.copy().columns
    ph_time = time_recov_unique.query("`Country/Region` == 'Philippines'")
    ph_time = ph_time[ph_time.columns[4:]]
    delta_recov = [0, *np.diff(ph_time.values.squeeze())]
    recov_time = ph_time.copy().columns
    ph_time = time_dead_unique.query("`Country/Region` == 'Philippines'")
    ph_time = ph_time[ph_time.columns[4:]]
    delta_dead = [0, *np.diff(ph_time.values.squeeze())]
    dead_time = ph_time.copy().columns

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=conf_time,
        y=delta_conf,
        name='Confirmed',
        marker_color=bs4_warning,
        mode='lines',
        text=list(map(lambda x: str(x) + ' new cases', delta_conf)),
    ))
    fig.add_trace(go.Scatter(
        x=dead_time,
        y=delta_dead,
        name='Deaths',
        marker_color=bs4_danger,
        mode='lines',
        text=list(map(lambda x: str(x) + ' new deaths', delta_recov)),
    ))
    fig.add_trace(go.Scatter(
        x=recov_time,
        y=delta_recov,
        name='Recovered',
        marker_color=bs4_success,
        mode='lines',
        text=list(map(lambda x: str(x) + ' new recoveries', delta_dead)),
    ))
    fig.update_layout(
        legend={
            'x': 0,
            'y': 1,
        },
        legend_orientation='h',
        margin={
            't': 0,
            'l': 0,
            'r': 0,
            'b': 0,
        },
        yaxis_title='new number of cases',
    )
    return plot(fig, output_type='div', include_plotlyjs=False)


def get_plot_by_age():
    try:
        ph_conf = data.get_ph_confirmed()
        conf_by_age = ph_conf.query("`RemovalType` == ''")['Age']
        conf_by_age = conf_by_age.groupby(pd.cut(conf_by_age, np.arange(0, 101, 10))).count()
        recov_by_age = ph_conf.query("`RemovalType` == 'Recovered'")['Age']
        recov_by_age = recov_by_age.groupby(pd.cut(recov_by_age, np.arange(0, 101, 10))).count()
        death_by_age = ph_conf.query("`RemovalType` == 'Died'")['Age']
        death_by_age = death_by_age.groupby(pd.cut(death_by_age, np.arange(0, 101, 10))).count()
    except (IndexError, ValueError, TypeError, KeyError):
        return settings.UNAVAILABLE_RESPONSE

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=conf_by_age.values,
            y=list(map(lambda x: str(x.left + 1) + '-' + str(x.right), conf_by_age.index.values)),
            text=conf_by_age,
            textposition='auto',
            name='Active',
            marker_color=bs4_warning,
            orientation='h',
        )
    )
    fig.add_trace(
        go.Bar(
            x=recov_by_age.values,
            y=list(map(lambda x: str(x.left + 1) + '-' + str(x.right), conf_by_age.index.values)),
            text=recov_by_age.values,
            name='Recovered',
            marker_color=bs4_success,
            orientation='h',
        )
    )
    fig.add_trace(
        go.Bar(
            x=death_by_age.values,
            y=list(map(lambda x: str(x.left + 1) + '-' + str(x.right), conf_by_age.index.values)),
            text=death_by_age.values,
            name='Deceased',
            marker_color=bs4_danger,
            orientation='h',
        )
    )
    fig.update_layout(
        barmode='stack',
        yaxis_title='age group',
        xaxis_title='number of cases',
        margin={
            't': 30,
            'l': 0,
            'r': 30,
            'b': 0,
        },
        yaxis={
          'categoryorder': 'category descending',
        },
        legend_orientation='h',
    )
    return plot(fig, output_type='div', include_plotlyjs=False)


def get_metro_cases():
    try:
        ph_cases = data.get_ph_confirmed()
    except (UndefinedVariableError, AttributeError, KeyError):
        return settings.UNAVAILABLE_RESPONSE

    metro_city_cases = (
        ph_cases
            .query("`RegionRes` == 'NCR'")
            .query("`RemovalType` == ''")
            .groupby('ProvCityRes')
            .count()
            .rename(index={'': 'For validation'})
    )['CaseCode']

    metro_city_recov = (
        ph_cases
            .query("`RegionRes` == 'NCR'")
            .query("`RemovalType` == 'Recovered'")
            .groupby('ProvCityRes')
            .count()
            .rename(index={'': 'For validation'})
    )['CaseCode']

    metro_city_death = (
        ph_cases
            .query("`RegionRes` == 'NCR'")
            .query("`RemovalType` == 'Died'")
            .groupby('ProvCityRes')
            .count()
            .rename(index={'': 'For validation'})
    )['CaseCode']

    city_names = [
        c.split('City of ')[-1]
        if 'City of' in c
        else c
        for c in metro_city_cases.index
    ]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=city_names,
        x=metro_city_cases.values,
        text=metro_city_cases.values,
        textposition='auto',
        name='Active',
        marker_color=bs4_warning,
        orientation='h',
    ))
    fig.add_trace(go.Bar(
        y=city_names,
        x=metro_city_recov.values,
        text=metro_city_recov.values,
        name='Recovered',
        marker_color=bs4_success,
        orientation='h',
    ))
    fig.add_trace(go.Bar(
        y=city_names,
        x=metro_city_death.values,
        text=metro_city_death.values,
        name='Deceased',
        marker_color=bs4_danger,
        orientation='h',
    ))
    fig.update_layout(
        margin={
            't': 30,
            'l': 0,
            'r': 0,
            'b': 0,
        },
        yaxis={
          'categoryorder': 'total ascending',
        },
        barmode='stack',
        legend_orientation='h',
    )
    return plot(fig, output_type='div', include_plotlyjs=False)
