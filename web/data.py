import geojson
import pandas as pd
import numpy as np
from urllib import request
from datetime import datetime
from django.core.cache import cache
from . import functions


def get_ph_confirmed():
    ph_conf = cache.get('ph_conf')
    if ph_conf is None:
        ph_url = 'https://ncovph.com/api/confirmed-cases'
        ph_conf = pd.read_json(request.urlopen(ph_url))
        ph_conf = ph_conf.drop('date_confirmed', axis=1)
        try:
            regions = [v['region'] if v is not None else None for v in ph_conf['residence'].values]
            provinces = [v['province'] if v is not None else None for v in ph_conf['residence'].values]
            cities = [v['city'] if v is not None else None for v in ph_conf['residence'].values]
            ph_conf.insert(8, 'region', regions)
            ph_conf.insert(9, 'province', provinces)
            ph_conf.insert(10, 'city', cities)
            ph_conf = ph_conf.drop('residence', axis=1)
        except IndexError:
            pass
        cache.set('ph_conf', ph_conf.to_json())
    else:
        ph_conf = pd.read_json(ph_conf)
    ph_conf = ph_conf.replace(np.nan, '')
    return ph_conf


def get_ph_geoapi():
    ph_conf_geo = cache.get('ph_conf_geo')
    if ph_conf_geo is None:
        ph_conf_geo = functions.df_to_geojson(ph_conf)
        cache.set('ph_conf_geo', ph_conf_geo)
        ph_conf_geo = pd.read_json(ph_conf_geo)
    else:
        ph_conf_geo = pd.read_json(ph_conf_geo)
    return ph_conf_geo


def get_ph_numbers():
    numbers = cache.get('numbers')
    if numbers is None:
        numbers_url = 'https://ncovph.com/api/counts'
        numbers = pd.read_json(request.urlopen(numbers_url), orient='index')
        numbers.rename(index={'deceased': 'deaths'}, inplace=True)
        numbers_type = numbers[0].index.to_list()
        numbers_count = numbers[0].fillna(0).astype(int).to_list()
        ph_numbers = dict(zip(numbers_type, numbers_count))
        cache.set('numbers', ph_numbers)
        cache.set('confirmed', ph_numbers['confirmed'], timeout=60*15)
        return ph_numbers
    return numbers


def get_ph_numbers_delta():
    numbers = get_ph_numbers()
    case_names = [
        'confirmed',
        'recovered',
        'deaths',
    ]
    time_unique = [
        get_confirmed_over_time(),
        get_recovered_over_time(),
        get_deaths_over_time(),
    ]
    delta = []

    for unique, name in zip(time_unique, case_names):
        ph_time = unique.query("`Country/Region` == 'Philippines'")
        ph_time = ph_time[ph_time.columns[4:]]
        ddelta = [0, *np.diff(ph_time.values.squeeze())]
        time = ph_time.copy().columns
        today_count = numbers[name]
        remote_count = ph_time[time[-1]].values[0]
        if today_count == remote_count:
            remote_count = ph_time[time[-2]].values[0]
        delta.append(today_count - remote_count)
    return dict(zip(case_names, delta))


def get_ph_hospitals():
    hospitals = cache.get('hospital')
    if hospitals is None:
        ph_conf = get_ph_confirmed()
        hospitals = ph_conf['facility'].value_counts()
        coordinates = []
        for x in hospitals.index:
            if '"' in x:
                coordinates.append(ph_conf.query(f"facility == '{x}'")['coordinates'].values[0])
            else:
                coordinates.append(ph_conf.query(f'facility == "{x}"')['coordinates'].values[0])
        hospitals = pd.DataFrame({'facility': hospitals.index, 'count': hospitals, 'coordinates': coordinates})
        hospitals.index = range(len(hospitals))
        cache.set('hospital', hospitals.to_json())
    else:
        hospitals = pd.read_json(hospitals)
    return hospitals


def get_confirmed_over_time():
    time_conf_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    time_conf = functions.date_to_datetime(pd.read_csv(request.urlopen(time_conf_url)))
    time_conf_unique = time_conf.groupby('Country/Region').sum()
    return time_conf_unique


def get_recovered_over_time():
    time_recov_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
    time_recov = functions.date_to_datetime(pd.read_csv(request.urlopen(time_recov_url)))
    time_recov_unique = time_recov.groupby('Country/Region').sum()
    return time_recov_unique


def get_deaths_over_time():
    time_dead_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    time_dead = functions.date_to_datetime(pd.read_csv(request.urlopen(time_dead_url)))
    time_dead_unique = time_dead.groupby('Country/Region').sum()
    return time_dead_unique


def get_world_daily():
    daily_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-26-2020.csv'
