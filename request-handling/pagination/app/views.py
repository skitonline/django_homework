from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

import csv


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    data = []
    with open(settings.BUS_STATION_CSV, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append({'Name': row['Name'],
                         'Street': row['Street'],
                         'District': row['District']})

    get_param = 'page'
    current_page = int(request.GET.get(get_param, 1))
    elements_per_page = 10
    paginator = Paginator(data, elements_per_page)
    page = paginator.page(current_page)

    if page.has_previous():
        prev_page_url = reverse('bus_stations')
        prev_page_url += f'?{get_param}={current_page - 1}'
    else:
        prev_page_url = None

    if page.has_next():
        next_page_url = reverse('bus_stations')
        next_page_url += f'?{get_param}={current_page + 1}'
    else:
        next_page_url = None

    return render(request, 'index.html', context={
        'bus_stations': page.object_list,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })

