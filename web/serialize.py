from numpy import diff
from web import data


bs4_success = '#00c851'
bs4_primary = '#4285f4',
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
    time_conf_unique = data.get_confirmed_over_time()
    time_recov_unique = data.get_recovered_over_time()
    time_dead_unique = data.get_deaths_over_time()

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
    ]

    return datasets