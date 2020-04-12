import json
import pytz
from . import data, plot, functions
from .models import *
from time import time
from datetime import datetime
from pandas import DataFrame
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render
from django.conf import settings
from django.utils.html import escapejs


LOCAL_TZ = pytz.timezone('Asia/Manila')
wake_time = time()

def index(request):
    ph_cases = data.get_ph_confirmed()
    hospitals = data.get_ph_hospitals()
    latest_announcement = Update.objects.order_by('-created').first()
    latest_announcement.created = (
        latest_announcement.created
            .replace(tzinfo=pytz.utc)
            .astimezone(LOCAL_TZ)
            .strftime("%d %b %Y")
        )
    if isinstance(ph_cases, DataFrame):
        ph_cases = escapejs(functions.df_to_geojson(ph_cases))
        hospitals = escapejs(functions.df_to_geojson(hospitals))
    else:
        ph_cases = None
        hospitals = None
    context = {
        'active_page': 'Dashboard',
        'announcement': latest_announcement,
        'age_plot': plot.get_plot_by_age(),
        'delta_counts': data.get_ph_numbers_delta(),
        'delta_plot': plot.get_delta_over_time(),
        'hospitals': hospitals,
        'last_updated': functions.check_last_updated(),
        'nationality_cases': plot.get_plot_by_nationality(),
        'ncr_cases': plot.get_metro_cases(),
        'numbers': data.get_ph_numbers(),
        'ph_cases': ph_cases,
        'time_plot': plot.get_plot_over_time(),
        'world_plot': plot.get_world_over_time(),
    }
    return render(request, 'web/index.html.j2', context)


def api_docs(request):
    context = {
        'active_page': 'API',
    }
    return render(request, 'web/api_docs.html.j2', context)


def api_name(request):
    if request.method == 'GET':
        response = {
            'name': 'ncovenience',
        }
        return JsonResponse(response)
    else:
        return HttpResponse(f'{request.method} not allowed')

def api(request, page):
    if request.method == 'GET':
        if page == 'health':
            response = {
                'uptime': time() - wake_time,
            }
            return JsonResponse(response)
        elif page == 'cases':
            ph_conf = data.get_ph_confirmed()
            ph_geo = functions.df_to_geojson(ph_conf)
            ph_geojson = json.loads(ph_geo)
            return JsonResponse(ph_geojson)
        elif page == 'hospitals':
            hospital = data.get_ph_hospitals()
            hosp_geo = functions.df_to_geojson(hospital)
            hosp_geojson = json.loads(hosp_geo)
            return JsonResponse(hosp_geojson)
        else:
            raise Http404()
    else:
        return HttpResponse(f'Cannot {request.method} on /api/{page}')
