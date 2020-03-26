from django.shortcuts import render
from django.conf import settings


def index(response):
    context = {
        'active_page': 'index',
    }
    return render(response, 'web/index.html.j2', context)
