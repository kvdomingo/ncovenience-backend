from json import loads
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from backend import functions, data, serialize


@require_GET
def cases(request):
    ph_conf = functions.df_to_geojson(data.get_phcovid())
    ph_json = loads(ph_conf)
    return JsonResponse(ph_json)


@require_GET
def numbers(request):
    number = data.get_ph_numbers()
    return JsonResponse(number)


@require_GET
def delta_counts(request):
    counts = data.get_ph_numbers_delta()
    return JsonResponse(counts)


@require_GET
def time_plot(request):
    datasets = serialize.get_plot_over_time()
    return JsonResponse(dict(datasets=datasets))


@require_GET
def delta_plot(request):
    datasets = serialize.get_delta_over_time()
    return JsonResponse(dict(datasets=datasets))


@require_GET
def world_plot(request):
    datasets = serialize.get_world_over_time()
    return JsonResponse(dict(datasets=datasets))


@require_GET
def age_plot(request):
    datasets = serialize.get_plot_by_age()
    return JsonResponse(dict(datasets=datasets))


@require_GET
def metro_plot(request):
    datasets = serialize.get_metro_cases()
    return JsonResponse(dict(datasets=datasets))
