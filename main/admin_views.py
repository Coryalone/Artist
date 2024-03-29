import math
import re, os, json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import PicturesForm
from django.forms import formset_factory

import requests
from main.models import Pictures


VK_USER_ID = os.getenv('VK_USER_ID')
VK_TOKEN = os.getenv('VK_TOKEN')


def get_photos_from_vk(offset=0, count=50):
    api = requests.get("https://api.vk.com/method/photos.getAll", params={
        'owner_id': VK_USER_ID,
        'access_token': VK_TOKEN,
        'offset': offset,
        'count': count,
        'photo_sizes': 0,
        'v': 5.103
    })
    return json.loads(api.text)


def get_fresh_photos(request):

    photos = []
    i = 0
    chunk_size = 50

    while True:
        response = get_photos_from_vk(offset=i, count=chunk_size)['response']
        raw_photos = response['items']
        count_photo = response["count"]

        if i > count_photo:
            break

        for raw_photo in raw_photos:
            new_photo = {}
            new_photo['id'] = raw_photo['id']
            new_photo['small_url'] = min(raw_photo['sizes'], key=lambda v: v['width'] if v['width'] > 600 else 1000000 - v['width'])['url']
            new_photo['big_url'] = max(raw_photo['sizes'], key=lambda v: v['width'])['url']
            new_photo['text'] = re.sub(r'#[\w]+', '', raw_photo['text'])
            new_photo['raw_text'] = raw_photo['text']
            photos.append(new_photo)

        i += chunk_size

    all_ids = get_all_ids()
    pocket = []
    lol_count = 0
    count_photo = count_photo - len(all_ids)

    for x in photos:
        if x['id'] not in all_ids:
            pocket.append(x)
            lol_count += 1
            if lol_count >= 12:
                break
    return pocket, count_photo

def get_all_ids():
    return [x['id_photo'] for x in list(Pictures.objects.values('id_photo'))]


@login_required()
def new_photos(request):
    fresh_photos, count_photo = get_fresh_photos(request)
    pictures_form = formset_factory(PicturesForm, extra=0)
    formset = pictures_form(request.POST or None, initial=[
        {'id_photo': x['id'], 'url_small': x['small_url'], 'url_big': x['big_url'], 'description': x['text'],
         'visible': x['raw_text'].lower().find('#главная') != -1,
         'category':  os.getenv('PORTRAITS') if x['raw_text'].lower().find('#портрет') != -1 else os.getenv('LANDSCAPES') if x['raw_text'].lower().find('#пейзаж') != -1 else \
         os.getenv('GRAPGIC') if x['raw_text'].lower().find('#графика') != -1 else os.getenv('SCULPTURES') if x['raw_text'].lower().find('#скульптур') != -1 else \
         os.getenv('MURALS') if x['raw_text'].lower().find('#настен') != -1 else os.getenv('DEFAULT')} for x in fresh_photos
    ])

    if formset.is_valid():
        for form in formset:
                Pictures.objects.create(**form.cleaned_data)
        return redirect('all_photos')

    context = {}
    context['formset'] = formset
    context['count_photo'] = count_photo
    return render(request, "new_photos.html", context)


@login_required()
def all_photos(request):
    page_number = 0
    if request.method == 'GET' and 'page' in request.GET:
        page_number = int(request.GET.get('page')) - 1
    page_size = 12
    page_started = page_number * page_size
    page_ended = page_started + page_size
    all_photos = list(Pictures.objects.all()[page_started:page_ended])
    count = Pictures.objects.all().count()
    pictures_form = formset_factory(PicturesForm, extra=0)
    formset = pictures_form(request.POST or None, initial=[
        {'id_photo': x.id_photo, 'url_small': x.url_small, 'url_big': x.url_big,
         'name': x.name, 'description': x.description,
         'visible': x.visible, 'not_upload': x.not_upload, 'category': x.category} for x in all_photos
    ])

    if formset.is_valid():
        for form in formset:
            for photo in all_photos:
                if form.cleaned_data['id_photo'] == photo.id_photo:
                    photo.id_photo = form.cleaned_data['id_photo']
                    photo.url_small = form.cleaned_data['url_small']
                    photo.url_big = form.cleaned_data['url_big']
                    photo.name = form.cleaned_data['name']
                    photo.description = form.cleaned_data['description']
                    photo.category = form.cleaned_data['category']
                    photo.visible = form.cleaned_data['visible']
                    photo.not_upload = form.cleaned_data['not_upload']
                    photo.save()

    context = {}
    context['formset'] = formset
    context['pages'] = range(1, math.ceil(count / page_size) + 1)
    context['current_page'] = page_number + 1
    return render(request, "all_photos.html", context)










