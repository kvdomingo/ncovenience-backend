import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import plot
from . import data


def get_plot_over_time():
    time_conf_unique = data.get_confirmed_over_time()
    time_recov_unique = data.get_recovered_over_time()
    time_dead_unique = data.get_deaths_over_time()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time_conf_unique.keys()[2:],
        y=time_conf_unique.query("`Country/Region` == 'Philippines'")[time_conf_unique.keys()[2:]].sum().values,
        name='Confirmed',
        marker_color='#ffbb33',
        mode='lines+markers',
    ))
    fig.add_trace(go.Scatter(
        x=time_recov_unique.keys()[2:],
        y=time_recov_unique.query("`Country/Region` == 'Philippines'")[time_recov_unique.keys()[2:]].sum().values,
        name='Recovered',
        marker_color='#00C851',
        mode='lines+markers',
    ))
    fig.add_trace(go.Scatter(
        x=time_dead_unique.keys()[2:],
        y=time_dead_unique.query("`Country/Region` == 'Philippines'")[time_dead_unique.keys()[2:]].sum().values,
        name='Deaths',
        marker_color='#ff4444',
        mode='lines+markers',
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
        xaxis_title='number of cases',
    )
    return plot(fig, output_type='div', include_plotlyjs=False)

def get_plot_by_age():
    ph_conf = data.get_ph_confirmed()
    valid_age = ph_conf['age'].drop(ph_conf.query("age == 'For Verification'").index).astype('uint8')
    conf_by_age = valid_age.groupby(pd.cut(valid_age, np.arange(10, 101, 10))).count()
    fig = go.Figure([
        go.Bar(
            x=conf_by_age.values,
            y=list(map(lambda x: str(x.left + 1) + '-' + str(x.right), conf_by_age.index.values)),
            text=conf_by_age.values,
            textposition='auto',
            name='Confirmed',
            marker_color='#ffbb33',
            orientation='h',
        ),
    ])
    fig.update_layout(
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
    )
    return plot(fig, output_type='div', include_plotlyjs=False)

def get_metro_cases():
    ph_conf = data.get_ph_confirmed()
    metro_conf = ph_conf.query("region == 'NCR'")
    fig = go.Figure(
        data=[
            go.Bar(
                y=metro_conf.groupby('city').count().index,
                x=metro_conf.groupby('city').count()['caseID'].values,
                text=metro_conf.groupby('city').count()['caseID'].values,
                textposition='auto',
                marker_color='#ffbb33',
                orientation='h',
            )
        ]
    )
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
    )
    return plot(fig, output_type='div', include_plotlyjs=False)
