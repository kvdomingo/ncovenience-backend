import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import plot
from datetime import datetime
from urllib import request
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache


daily_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-25-2020.csv'
time_conf_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
time_recov_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
time_dead_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
time_conf = pd.read_csv(request.urlopen(time_conf_url))
time_recov = pd.read_csv(request.urlopen(time_recov_url))
time_dead = pd.read_csv(request.urlopen(time_dead_url))
world_daily = pd.read_csv(request.urlopen(daily_url))

ph_conf = cache.get('ph_conf')
if ph_conf is None:
    ph_url = 'https://ncovph.com/api/confirmed-cases'
    ph_conf = pd.read_json(request.urlopen(ph_url))
    cache.set('ph_conf', ph_conf.to_json())
else:
    ph_conf = pd.read_json(ph_conf)


def index(request):
    context = {
        'active_page': 'index',
    }
    return render(request, 'web/index.html.j2', context)


def data(request):
    fig = px.scatter_geo(
        data_frame=world_daily,
        lat='Lat',
        lon='Long_',
        hover_name='Country_Region',
        hover_data=['Confirmed'],
        size=np.log10(world_daily['Confirmed']).replace(np.nan, 0).replace(np.inf, 0).replace(-np.inf, 0),
        projection='natural earth',
    )
    world_daily_map = plot(fig, output_type='div', include_plotlyjs=False)

    world_unique = time_conf.groupby('Country/Region').sum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=world_unique.keys()[2:],
        y=world_unique[world_unique.keys()[2:]].sum().values,
        name='TOTAL',
    ))
    for i in range(len(world_unique)):
        fig.add_trace(go.Scatter(
            x=world_unique.keys()[2:],
            y=world_unique[world_unique.columns[2:]].values[i],
            name=world_unique.index[i],
        ))
    world_daily_plot = plot(fig, output_type='div', include_plotlyjs=False)

    context = {
        'active_page': 'data',
        'ph_conf': ph_conf.to_html(),
        'world_daily_map': world_daily_map,
        'world_daily_plot': world_daily_plot,
    }
    return render(request, 'web/data.html.j2', context)


def api(request):
    return JsonResponse(ph_conf.to_dict('index'))
