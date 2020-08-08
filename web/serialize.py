from numpy import arange, diff, round, nan
from pandas import cut, Series
from web.data import get_confirmed_over_time,\
                     get_recovered_over_time,\
                     get_deaths_over_time,\
                     get_phcovid


bs4_success = '#00c851'
bs4_primary = '#4285f4',
bs4_warning = '#ffbb33'
bs4_danger = '#ff4444'

def get_plot_over_time():
    time_conf_unique = get_confirmed_over_time()
    time_recov_unique = get_recovered_over_time()
    time_dead_unique = get_deaths_over_time()

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

    time_active_keys = time_conf_keys.copy()
    time_active_vals = time_conf_vals - time_recov_vals - time_dead_vals

    datasets = [
        dict(
            label="Confirmed",
            data=[dict(x=k, y=int(v)) for k, v in zip(list(time_conf_keys), time_conf_vals)],
            borderColor=bs4_warning,
        ),
        dict(
            label="Active",
            data=[dict(x=k, y=int(v)) for k, v in zip(list(time_active_keys), time_active_vals)],
            borderColor=bs4_primary,
        ),
        dict(
            label="Recovered",
            data=[dict(x=k, y=int(v)) for k, v in zip(list(time_recov_keys), time_recov_vals)],
            borderColor=bs4_success,
        ),
        dict(
            label="Deceased",
            data=[dict(x=k, y=int(v)) for k, v in zip(list(time_dead_keys), time_dead_vals)],
            borderColor=bs4_danger,
        ),
    ]

    return datasets


def get_delta_over_time():
    time_conf_unique = get_confirmed_over_time()
    time_recov_unique = get_recovered_over_time()
    time_dead_unique = get_deaths_over_time()

    ph_time = time_conf_unique.query("`Country/Region` == 'Philippines'")
    ph_time = ph_time[ph_time.columns[4:]]
    delta_conf = [0, *diff(ph_time.values.squeeze())]
    conf_time = ph_time.copy().columns
    ph_time = time_recov_unique.query("`Country/Region` == 'Philippines'")
    ph_time = ph_time[ph_time.columns[4:]]
    delta_recov = [0, *diff(ph_time.values.squeeze())]
    recov_time = ph_time.copy().columns
    ph_time = time_dead_unique.query("`Country/Region` == 'Philippines'")
    ph_time = ph_time[ph_time.columns[4:]]
    delta_dead = [0, *diff(ph_time.values.squeeze())]
    dead_time = ph_time.copy().columns

    datasets = [
        dict(
            label="Confirmed",
            data=[dict(x=k, y=int(v)) for k, v in zip(list(conf_time), delta_conf)],
            borderColor=bs4_warning,
        ),
        dict(
            label="Recovered",
            data=[dict(x=k, y=int(v)) for k, v in zip(list(recov_time), delta_recov)],
            borderColor=bs4_success,
        ),
        dict(
            label="Deceased",
            data=[dict(x=k, y=int(v)) for k, v in zip(list(dead_time), delta_dead)],
            borderColor=bs4_danger,
        ),
    ]

    return datasets


def get_world_over_time():
    time_conf_unique = get_confirmed_over_time()
    time_recov_unique = get_recovered_over_time()
    time_dead_unique = get_deaths_over_time()

    time_conf_unique = time_conf_unique[time_conf_unique.columns[2:]]
    world_conf = time_conf_unique.sum()/1e6

    time_recov_unique = time_recov_unique[time_recov_unique.columns[2:]]
    world_recov = time_recov_unique.sum()/1e6

    time_dead_unique = time_dead_unique[time_dead_unique.columns[2:]]
    world_dead = time_dead_unique.sum()/1e6

    datasets = [
        dict(
            label="Confirmed",
            data=[dict(x=k, y=float(v)) for k, v in zip(list(time_conf_unique), world_conf)],
            borderColor=bs4_warning,
        ),
        dict(
            label="Recovered",
            data=[dict(x=k, y=float(v)) for k, v in zip(list(time_recov_unique), world_recov)],
            borderColor=bs4_success,
        ),
        dict(
            label="Deceased",
            data=[dict(x=k, y=float(v)) for k, v in zip(list(time_dead_unique), world_dead)],
            borderColor=bs4_danger,
        ),
    ]
    return datasets


def get_plot_by_age():
    ph_conf = get_phcovid()
    categories = ['', 'Recovered', 'Died']
    conf_by_age = ph_conf.query("`status` == ''").age
    conf_by_age = conf_by_age.groupby(cut(conf_by_age, arange(0, 86, 5), right=False)).count()
    conf_by_age.index = conf_by_age.index.to_native_types()
    recov_by_age = ph_conf.query("`status` == 'Recovered'").age
    recov_by_age = recov_by_age.groupby(cut(recov_by_age, arange(0, 86, 5), right=False)).count()
    recov_by_age.index = recov_by_age.index.to_native_types()
    death_by_age = ph_conf.query("`status` == 'Died'").age
    death_by_age = death_by_age.groupby(cut(death_by_age, arange(0, 86, 5), right=False)).count()
    death_by_age.index = death_by_age.index.to_native_types()

    total_age_2010 = {
        "[0, 5)": 1166028,
        "[5, 10)": 1136020,
        "[10, 15)": 1113945,
        "[15, 20)": 1155098,
        "[20, 25)": 1203514,
        "[25, 30)": 1159327,
        "[30, 35)": 1026428,
        "[35, 40)": 852455,
        "[40, 45)": 752861,
        "[45, 50)": 634135,
        "[50, 55)": 527312,
        "[55, 60)": 386578,
        "[60, 65)": 279192,
        "[65, 70)": 154754,
        "[70, 75)": 113229,
        "[75, 80)": 68749,
        "[80, 85)": 62203,
    }
    total_age_2010 = Series(
        index=list(total_age_2010.keys()),
        data=list(total_age_2010.values())
    )

    conf_age_norm = (round(conf_by_age/total_age_2010 * 100000)
        .rename(lambda x: '-'.join(x.strip('[').strip(')').split(', ')))
        .rename(index={'80-85': '80+'}))
    recov_age_norm = (round(recov_by_age/total_age_2010 * 100000)
        .rename(lambda x: '-'.join(x.strip('[').strip(')').split(', ')))
        .rename(index={'80-85': '80+'}))
    death_age_norm = (round(death_by_age/total_age_2010 * 100000)
        .rename(lambda x: '-'.join(x.strip('[').strip(')').split(', ')))
        .rename(index={'80-85': '80+'}))

    data = dict(
        labels=list(conf_age_norm.index),
        datasets = [
            dict(
                label="Confirmed",
                data=[int(v) for v in conf_age_norm.values],
                backgroundColor=bs4_warning,
            ),
            dict(
                label="Recovered",
                data=[int(v) for v in recov_age_norm.values],
                backgroundColor=bs4_success,
            ),
            dict(
                label="Deceased",
                data=[int(v) for v in death_age_norm.values],
                backgroundColor=bs4_danger,
            ),
        ]
    )
    return data


def get_metro_cases():
    ph_cases = get_phcovid()

    metro_city_cases = (
        ph_cases
            .query("`status` == ''")
            .residence
    )
    metro_city_cases = (
        metro_city_cases[
            metro_city_cases
                .str.contains('Metro Manila')
        ]
            .str.split(', ')
            .str[0]
            .value_counts()
            .drop('Metro Manila')
    )

    metro_city_recov = (
        ph_cases
            .query("`status` == 'Recovered'")
            .residence
    )
    metro_city_recov = (
        metro_city_recov[
            metro_city_recov
                .str.contains('Metro Manila')
        ]
            .str.split(', ')
            .str[0]
            .value_counts()
            .drop('Metro Manila')
    )

    metro_city_death = (
        ph_cases
            .query("`status` == 'Died'")
            .residence
    )
    metro_city_death = (
        metro_city_death[
            metro_city_death
                .str.contains('Metro Manila')
        ]
            .str.split(', ')
            .str[0]
            .value_counts()
            .drop('Metro Manila')
    )

    metro_pop_2015 = {
        'Manila City': 1780148,
        'Mandaluyong City': 386276,
        'Marikina City': 450741,
        'Pasig City': 755300,
        'Quezon City': 2936116,
        'San Juan City': 122180,
        'Caloocan City': 1583978,
        'Malabon City': 365525,
        'Navotas City': 249463,
        'Valenzuela City': 620422,
        'Las Piñas City': 588894,
        'Makati City': 582602,
        'Muntinlupa City': 504509,
        'Parañaque City': 665822,
        'Pasay City': 416522,
        'Pateros': 63840,
        'Taguig City': 804915,
    }

    metro_pop = Series(
        data=list(metro_pop_2015.values()),
        index=list(metro_pop_2015.keys())
    )

    metro_conf_norm = round(metro_city_cases/metro_pop * 100000).replace(nan, 0)
    metro_recov_norm = round(metro_city_recov/metro_pop * 100000).replace(nan, 0)
    metro_dead_norm = round(metro_city_death/metro_pop * 100000).replace(nan, 0)

    data = dict(
        labels=list(metro_conf_norm.index),
        datasets=[
            dict(
                label="Confirmed",
                data=[int(v) for v in metro_conf_norm.values],
                backgroundColor=bs4_warning,
            ),
            dict(
                label="Recovered",
                data=[int(v) for v in metro_recov_norm.values],
                backgroundColor=bs4_success,
            ),
            dict(
                label="Deceased",
                data=[int(v) for v in metro_dead_norm.values],
                backgroundColor=bs4_danger,
            ),
        ]
    )
    return data
