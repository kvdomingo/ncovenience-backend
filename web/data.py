import geojson
import pandas as pd
import numpy as np
from urllib import request
from datetime import datetime
from django.core.cache import cache


def df_to_geojson(df):
    features = []
    def insert_features(row):
        try:
            features.append(geojson.Feature(
                geometry=geojson.Point((
                    row['coordinates']['lng'],
                    row['coordinates']['lat'],
                    0,
                )),
                properties=row.to_dict(),
            ))
        except KeyError:
            features.append(geojson.Feature(
                geometry=geojson.Point((
                    row['longitude'],
                    row['latitude'],
                    0,
                )),
                properties=row.to_dict(),
            ))
    df.apply(insert_features, axis=1)
    return geojson.dumps(geojson.FeatureCollection(features, separators=(',', ':')))

def date_to_datetime(df):
    for d in df.columns[4:]:
        df = df.rename(columns={d: datetime.strptime(d, '%m/%d/%y')})
    return df

def count_latest(df):
    df_unique = df.groupby('Country/Region').sum()
    total = df_unique[df_unique.keys()[-1]][df_unique.index.tolist().index('Philippines')]
    return total

def get_ph_confirmed():
    ph_conf = cache.get('ph_conf')
    if ph_conf is None:
        ph_url = 'https://ncovph.com/api/confirmed-cases'
        ph_conf = pd.read_json(request.urlopen(ph_url))
        ph_conf = ph_conf.drop('date_confirmed', axis=1)
        regions, provinces, cities = [], [], []
        for v in ph_conf['residence'].values:
            if v is not None:
                regions.append(v['region'])
                provinces.append(v['province'])
                cities.append(v['city'])
            else:
                regions.append(None)
                provinces.append(None)
                cities.append(None)
        ph_conf.insert(8, 'region', regions)
        ph_conf.insert(9, 'province', provinces)
        ph_conf.insert(10, 'city', cities)
        ph_conf = ph_conf.drop('residence', axis=1)
        cache.set('ph_conf', ph_conf.to_json())
    else:
        ph_conf = pd.read_json(ph_conf)
    ph_conf = ph_conf.replace(np.nan, '')
    return ph_conf

def get_ph_geoapi():
    ph_conf_geo = cache.get('ph_conf_geo')
    if ph_conf_geo is None:
        ph_conf_geo = df_to_geojson(ph_conf)
        cache.set('ph_conf_geo', ph_conf_geo)
        ph_conf_geo = pd.read_json(ph_conf_geo)
    else:
        ph_conf_geo = pd.read_json(ph_conf_geo)
    return ph_conf_geo

def get_ph_numbers():
    numbers = cache.get('numbers')
    if numbers is None:
        numbers_url = 'https://ncov-tracker-slexwwreja-de.a.run.app/numbers'
        numbers = pd.read_json(request.urlopen(numbers_url))
        cache.set('numbers', numbers.to_json())
    else:
        numbers = pd.read_json(numbers)
    return numbers

def get_ph_hospitals():
    hospitals = cache.get('hospital')
    if hospitals is None:
        ph_conf = get_ph_confirmed()
        hospitals = ph_conf['facility'].value_counts()
        hospitals['For validation'] += hospitals['']
        hospitals = hospitals.drop('')
        coordinates = [ph_conf.query(f'facility == "{x}"')['coordinates'].values[0] for x in hospitals.index]
        hospitals = pd.DataFrame({'facility': hospitals.index, 'count': hospitals, 'coordinates': coordinates})
        hospitals.index = range(len(hospitals))
        cache.set('hospital', hospitals.to_json())
    else:
        hospitals = pd.read_json(hospitals)
    return hospitals

def get_confirmed_over_time():
    time_conf_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    time_conf = date_to_datetime(pd.read_csv(request.urlopen(time_conf_url)))
    time_conf_unique = time_conf.groupby('Country/Region').sum()
    return time_conf_unique

def get_recovered_over_time():
    time_recov_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
    time_recov = date_to_datetime(pd.read_csv(request.urlopen(time_recov_url)))
    time_recov_unique = time_recov.groupby('Country/Region').sum()
    return time_recov_unique

def get_deaths_over_time():
    time_dead_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    time_dead = date_to_datetime(pd.read_csv(request.urlopen(time_dead_url)))
    time_dead_unique = time_dead.groupby('Country/Region').sum()
    return time_dead_unique

def get_world_daily():
    daily_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-26-2020.csv'
