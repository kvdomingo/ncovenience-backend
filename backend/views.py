from json import loads
from django.http import JsonResponse
from web import data, functions, serialize


def cases(request):
    if request.method == 'GET':
        ph_conf = functions.df_to_geojson(data.get_phcovid())
        ph_json = loads(ph_conf)
        return JsonResponse(ph_json)


def numbers(request):
    if request.method == 'GET':
        number = data.get_ph_numbers()
        return JsonResponse(number)


def delta_counts(request):
    if request.method == 'GET':
        counts = data.get_ph_numbers_delta()
        return JsonResponse(counts)


def time_plot(request):
    if request.method == 'GET':
        datasets = serialize.get_plot_over_time()
        return JsonResponse(dict(datasets=datasets))


def delta_plot(request):
    if request.method == 'GET':
        datasets = serialize.get_delta_over_time()
        return JsonResponse(dict(datasets=datasets))


def world_plot(request):
    if request.method == 'GET':
        datasets = serialize.get_world_over_time()
        return JsonResponse(dict(datasets=datasets))


def age_plot(request):
    if request.method == 'GET':
        datasets = serialize.get_plot_by_age()
        return JsonResponse(dict(datasets=datasets))