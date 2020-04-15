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


wake_time = time()

def index(request):
    latest_announcement = Update.objects.order_by('-created').first()
    latest_announcement.created = (
        latest_announcement.created
            .replace(tzinfo=pytz.utc)
            .astimezone(settings.LOCAL_TZ)
            .strftime("%d %b %Y")
    )
    context = {
        'active_page': 'Dashboard',
        'announcement': latest_announcement,
        'age_plot': plot.get_plot_by_age(),
        'delta_counts': data.get_ph_numbers_delta(),
        'delta_plot': plot.get_delta_over_time(),
        'last_updated': functions.check_last_updated(),
        'ncr_cases': plot.get_metro_cases(),
        'numbers': data.get_ph_numbers(),
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
            ph_json = ph_conf.to_dict('index')
            return JsonResponse(ph_json)
        else:
            raise Http404()
    else:
        return HttpResponse(f'Cannot {request.method} on /api/{page}')
