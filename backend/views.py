import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from web import data, functions, plot


def cases(request):
    if request.method == 'GET':
        ph_conf = functions.df_to_geojson(data.get_phcovid())
        ph_json = json.loads(ph_conf)
        return JsonResponse(ph_json)

def numbers(request):
    if request.method == 'GET':
        numbers = data.get_ph_numbers()
        return JsonResponse(numbers)

def delta_counts(request):
    if request.method == 'GET':
        counts = data.get_ph_numbers_delta()
        return JsonResponse(counts)

def time_plot(request):
    if request.method == 'GET':
        data = plot.get_plot_over_time()
        return JsonResponse({'plot': data})
