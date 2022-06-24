from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
import csv

from pagination.settings import BUS_STATION_CSV


with open(BUS_STATION_CSV, newline='', encoding='utf-8') as file:
    CONTENT = list(csv.DictReader(file))


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(CONTENT, 10)
    page = paginator.get_page(page_number)
    context = {
        'bus_stations': page.object_list,
        'page': page
    }
    return render(request, 'stations/index.html', context)
