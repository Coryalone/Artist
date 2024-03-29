import os
import random

from django.http import JsonResponse
from django.shortcuts import render

from main.models import Pictures


def api_photos_by_category(request, category):
    filtered_photos = Pictures.objects.all().filter(category=category)
    response = [{'id_photo': x.id_photo, 'url_small': x.url_small, 'url_big': x.url_big,
         'name': x.name, 'description': x.description} for x in filtered_photos]
    return JsonResponse({'data': response})


def api_shuffled_main_page_photos(request):
    filtered_photos = Pictures.objects.all().filter(visible=True)
    response = [{'id_photo': x.id_photo, 'url_small': x.url_small, 'url_big': x.url_big,
          'name': x.name, 'description': x.description} for x in filtered_photos]
    random.shuffle(response)
    return JsonResponse({'data': response})


def main_page(request):
    return render(request, "index.html")


def portraits(request):
    return render(request, "portraits.html", context={'key': os.getenv('PORTRAITS')})


def landscapes(request):
    return render(request, "landscapes.html", context={'key': os.getenv('LANDSCAPES')})


def graphics(request):
    return render(request, "graphics.html", context={'key': os.getenv('GRAPGIC')})


def sculptures(request):
    return render(request, "sculptures.html", context={'key': os.getenv('SCULPTURES')})


def murals(request):
    return render(request, "murals.html", context={'key': os.getenv('MURALS')})


def about(request):
    return render(request, "about.html")
