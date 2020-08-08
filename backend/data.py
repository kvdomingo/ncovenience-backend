import os
import pandas as pd
import numpy as np
from urllib import request
from urllib.error import HTTPError
from django.core.cache import cache
from django.conf import settings
from backend import functions


def get_ph_confirmed():
    ph_conf = cache.get('ph_conf')
    if ph_conf is None:
        ph_url = 'https://raw.githubusercontent.com/benhur07b/covid19ph-doh-data-dump/master/data/case-information.csv'
        try:
            ph_conf = pd.read_csv(request.urlopen(ph_url))
            cache.set('ph_conf', ph_conf.to_json(), timeout=settings.DEFAULT_TIMEOUT)
        except HTTPError:
            return settings.UNAVAILABLE_RESPONSE
    else:
        ph_conf = pd.read_json(ph_conf)
    ph_conf = ph_conf.replace(np.nan, '')
    return ph_conf


def get_phcovid():
    with open(os.path.join(settings.BASE_DIR, 'backend/data/latest.json'), 'r') as f:
        df = pd.read_json(f, orient='index').replace(np.nan, '').replace('None', '')
    return df


def get_ph_numbers():
    numbers = cache.get('numbers')
    if numbers is None:
        numbers_type = [
            'confirmed',
            'active',
            'recovered',
            'deceased',
        ]
        ph_cases = [
            get_confirmed_over_time(),
            get_recovered_over_time(),
            get_deaths_over_time(),
        ]
        ph_cases = [pc.query('`Country/Region` == "Philippines"') for pc in ph_cases]
        numbers_count = [pc[pc.columns[-1]].values[0] for pc in ph_cases]
        numbers_count.insert(1, numbers_count[0] - numbers_count[1] - numbers_count[2])
        numbers_count = [int(nc) for nc in numbers_count]
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
        'deceased',
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
    case_names.insert(1, 'active')
    delta.insert(1, delta[0] - delta[1] - delta[2])
    delta = [int(d) for d in delta]
    return dict(zip(case_names, delta))


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
