import json
from . import data, plot
from time import time
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render
from django.conf import settings
from django.utils.html import escapejs


wake_time = time()

def index(request):
    numbers = data.get_ph_numbers()
    ph_hosp = data.df_to_geojson(data.get_ph_hospitals())
    ph_geo = data.df_to_geojson(data.get_ph_confirmed())
    context = {
        'active_page': 'index',
        'num_confirmed': numbers.query("`type` == 'confirmed'")['count'].values[0],
        'num_recovered': numbers.query("`type` == 'recovered'")['count'].values[0],
        'num_death': numbers.query("`type` == 'deaths'")['count'].values[0],
        'num_tests': numbers.query("`type` == 'tests'")['count'].values[0],
        'num_pum': numbers.query("`type` == 'PUMs'")['count'].values[0],
        'num_pui': numbers.query("`type` == 'PUIs'")['count'].values[0],
        'time_plot': plot.get_plot_over_time(),
        'delta_plot': plot.get_delta_over_time(),
        'age_plot': plot.get_plot_by_age(),
        'ncr_cases': plot.get_metro_cases(),
        'nationality_cases': plot.get_plot_by_nationality(),
        'ph_cases': escapejs(ph_geo),
        'hospitals': escapejs(ph_hosp),
    }
    return render(request, 'web/index.html.j2', context)


def api_health(request):
    if request.method == 'GET':
        health = {
            'name': 'ncovenience',
            'uptime': time() - wake_time,
        }
        return JsonResponse(health)
    else:
        return HttpResponse(f'{request.method} not allowed')

def api(request, page):
    if request.method == 'GET':
        if page == 'cases':
            ph_conf = data.get_ph_confirmed()
            ph_geo = data.df_to_geojson(ph_conf)
            ph_geojson = json.loads(ph_geo)
            return JsonResponse(ph_geojson)
        elif page == 'hospitals':
            hospital = data.get_ph_hospitals()
            hosp_geo = data.df_to_geojson(hospital)
            hosp_geojson = json.loads(hosp_geo)
            return JsonResponse(hosp_geojson)
        else:
            raise Http404()
    else:
        return HttpResponse(f'Cannot {request.method} on /api/{page}')
