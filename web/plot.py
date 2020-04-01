import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import plot
from . import data


bs4_success = '#00c851'
bs4_warning = '#ffbb33'
bs4_danger = '#ff4444'

def get_plot_over_time():
    time_conf_unique = data.get_confirmed_over_time()
    time_recov_unique = data.get_recovered_over_time()
    time_dead_unique = data.get_deaths_over_time()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time_conf_unique.keys()[2:],
        y=time_conf_unique.query("`Country/Region` == 'Philippines'")[time_conf_unique.keys()[2:]].sum().values,
        name='Confirmed',
        marker_color=bs4_warning,
        mode='lines',
    ))
    fig.add_trace(go.Scatter(
        x=time_recov_unique.keys()[2:],
        y=time_recov_unique.query("`Country/Region` == 'Philippines'")[time_recov_unique.keys()[2:]].sum().values,
        name='Recovered',
        marker_color=bs4_success,
        mode='lines',
    ))
    fig.add_trace(go.Scatter(
        x=time_dead_unique.keys()[2:],
        y=time_dead_unique.query("`Country/Region` == 'Philippines'")[time_dead_unique.keys()[2:]].sum().values,
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
    ph_conf = data.get_ph_confirmed()
    valid_age = ph_conf['age'].drop(ph_conf.query("age == 'For Verification'").index).astype('uint8')
    recov_by_age = ph_conf.drop(ph_conf.query("age == 'For Verification'").index).query("status == 'Recovered'")
    recov_by_age = recov_by_age['age'].drop(recov_by_age.query("age == 'For Verification'").index).astype('uint8')
    recov_by_age = recov_by_age.groupby(pd.cut(recov_by_age, np.arange(10, 101, 10))).count()
    death_by_age = ph_conf.drop(ph_conf.query("age == 'For Verification'").index).query("status == 'Deceased'")
    death_by_age = death_by_age['age'].drop(death_by_age.query("age == 'For Verification'").index).astype('uint8')
    death_by_age = death_by_age.groupby(pd.cut(death_by_age, np.arange(10, 101, 10))).count()
    conf_by_age = ph_conf.drop(ph_conf.query("age == 'For Verification'").index)
    conf_by_age = conf_by_age['age'].drop(conf_by_age.query("age == 'For Verification'").index).astype('uint8')
    conf_by_age = conf_by_age.groupby(pd.cut(conf_by_age, np.arange(10, 101, 10))).count()
    cases_by_age = conf_by_age.values - recov_by_age.values - death_by_age.values

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=cases_by_age,
            y=list(map(lambda x: str(x.left + 1) + '-' + str(x.right), conf_by_age.index.values)),
            text=cases_by_age,
            textposition='auto',
            name='Confirmed',
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
    ph_conf = data.get_ph_confirmed()
    metro_conf = ph_conf.query("region == 'NCR'")
    metro_city_recov = metro_conf.query("status == 'Recovered'").groupby('city').count()['caseID']
    metro_city_death = metro_conf.query("status == 'Deceased'").groupby('city').count()['caseID']
    metro_city_cases = metro_conf.query("status == 'Unspecified'").groupby('city').count()['caseID']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=metro_city_cases.index,
        x=metro_city_cases.values,
        text=metro_city_cases.values,
        textposition='auto',
        name='Confirmed',
        marker_color=bs4_warning,
        orientation='h',
    ))
    fig.add_trace(go.Bar(
        y=metro_city_recov.index,
        x=metro_city_recov.values,
        text=metro_city_recov.values,
        name='Recovered',
        marker_color=bs4_success,
        orientation='h',
    ))
    fig.add_trace(go.Bar(
        y=metro_city_death.index,
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
          'categoryorder': 'category descending',
        },
        barmode='stack',
        legend_orientation='h',
    )
    return plot(fig, output_type='div', include_plotlyjs=False)

def get_plot_by_nationality():
    ph_conf = data.get_ph_confirmed()
    nationality = ph_conf['nationality'].value_counts()
    nat = nationality.index.to_list()
    nat[1] = 'For validation'
    nationality.index = nat

    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=nationality.index,
        values=nationality.values,
    ))
    fig.update_traces(
        textinfo='value+label',
        textposition='none',
    )
    fig.update_layout(
        uniformtext_mode='hide',
        margin={
            't': 0,
            'l': 0,
            'r': 0,
            'b': 0,
        },
    )
    return plot(fig, output_type='div', include_plotlyjs=False)
