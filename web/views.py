import os
import json
import geojson
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
from dotenv import load_dotenv


load_dotenv()
px.set_mapbox_access_token(os.environ['MAPBOX_ACCESS_TOKEN'])


def df_to_geojson(df):
    features = []
    insert_features = lambda row: features.append(geojson.Feature(
            geometry=geojson.Point((
                row['coordinates']['lng'],
                row['coordinates']['lat'],
                0,
            )),
            properties=row.to_dict(),
        ))
    df.apply(insert_features, axis=1)
    return geojson.dumps(geojson.FeatureCollection(features))


def date_to_datetime(df):
    for d in df.columns[4:]:
        df = df.rename(columns={d: datetime.strptime(d, '%m/%d/%y')})
    return df


def count_latest(df):
    df_unique = df.groupby('Country/Region').sum()
    total = df_unique[df_unique.keys()[-1]][df_unique.index.tolist().index('Philippines')]
    return total


daily_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-26-2020.csv'
time_conf_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
time_recov_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
time_dead_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'

time_conf = date_to_datetime(pd.read_csv(request.urlopen(time_conf_url)))
time_recov = date_to_datetime(pd.read_csv(request.urlopen(time_recov_url)))
time_dead = date_to_datetime(pd.read_csv(request.urlopen(time_dead_url)))
world_daily = pd.read_csv(request.urlopen(daily_url))

ph_conf = cache.get('ph_conf')
if ph_conf is None:
    ph_url = 'https://ncovph.com/api/confirmed-cases'
    ph_conf = pd.read_json(request.urlopen(ph_url))
    ph_conf = ph_conf.drop('date_confirmed', axis=1)
    cache.set('ph_conf', ph_conf.to_json())
else:
    ph_conf = pd.read_json(ph_conf)

ph_conf_geo = cache.get('ph_conf_geo')
if ph_conf_geo is None:
    ph_conf_geo = df_to_geojson(ph_conf)
    cache.set('ph_conf_geo', ph_conf_geo)
    ph_conf_geo = pd.read_json(ph_conf_geo)
else:
    ph_conf_geo = pd.read_json(ph_conf_geo)

numbers = cache.get('numbers')
if numbers is None:
    numbers_url = 'https://ncov-tracker-slexwwreja-de.a.run.app/numbers'
    numbers = pd.read_json(numbers_url)
    cache.set('numbers', numbers.to_json())
else:
    numbers = pd.read_json(numbers)


def index(request):
    time_conf_unique = time_conf.groupby('Country/Region').sum()
    time_recov_unique = time_recov.groupby('Country/Region').sum()
    time_dead_unique = time_dead.groupby('Country/Region').sum()

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
    time_plot = plot(fig, output_type='div', include_plotlyjs=False)

    conf_by_age = ph_conf.groupby(pd.cut(ph_conf['age'], np.arange(10, 101, 10))).count()
    fig = go.Figure([
        go.Bar(
            x=conf_by_age['caseID'].values[::-1],
            y=list(map(lambda x: str(x.left + 1) + '-' + str(x.right), conf_by_age.index.values))[::-1],
            text=conf_by_age['caseID'].values,
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
            't': 0,
            'l': 0,
            'r': 0,
            'b': 0,
        },
    )
    age_plot = plot(fig, output_type='div', include_plotlyjs=False)

    context = {
        'active_page': 'index',
        'num_confirmed': numbers.query("type == 'confirmed'")['count'].values[0],
        'num_recovered': numbers.query("type == 'recovered'")['count'].values[0],
        'num_death': numbers.query("type == 'deaths'")['count'].values[0],
        'num_tests': numbers.query("type == 'tests'")['count'].values[0],
        'num_pum': numbers.query("type == 'PUMs'")['count'].values[0],
        'num_pui': numbers.query("type == 'PUIs'")['count'].values[0],
        'time_plot': time_plot,
        'age_plot': age_plot,
    }
    return render(request, 'web/index.html.j2', context)


def data(request):
    context = {
        'active_page': 'data',
        'ph_conf': ph_conf.to_html(),
    }
    return render(request, 'web/data.html.j2', context)


def api(request):
    return JsonResponse(ph_conf.to_dict('index'))


def api_geo(request):
    return JsonResponse(json.loads(df_to_geojson(ph_conf)))
