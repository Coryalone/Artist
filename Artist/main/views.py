import re, os, json, time, random

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import GeeksForm
from django.forms import formset_factory

import requests
from main.forms import PostForm
from main.models import Pictures


VK_USER_ID = '62391816'
VK_TOKEN = os.getenv('VK_TOKEN')


def get_photo_data(offset=0, count=50):
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
    urls_set = set()

    photos = []

    data = get_photo_data()
    count_photo = data["response"]["count"]
    i = 0
    w = 0
    count = 50
    while i <= count_photo:
        raw_photos = get_photo_data(offset=i, count=count)['response']['items']
        for dick in raw_photos:
            new_photo = {}

            new_photo['id'] = dick['id']
            for item in dick['sizes']:
                if item['type'] == 'm':
                    new_photo['small_url'] = item['url']
                elif item['type'] == 'x':
                    new_photo['big_url'] = item['url']

            photos.append(new_photo)

        i += count

    all_ids = get_all_ids()
    fresh_photos = []

    for photo in photos:
        if photo['id'] not in all_ids:
            fresh_photos.append(photo)

    return fresh_photos


def get_all_ids():
    check_list = list(Pictures.objects.values('id_photo'))
    pay_list = []
    for i in check_list:
        pay_list.append(i['id_photo'])
    return pay_list


def new_photos(request):
    context = {}
    spisok = get_fresh_photos(request)

    GeeksFormSet = formset_factory(GeeksForm, extra=0)
    formset = GeeksFormSet(request.POST or None, initial=[
        {'id_photo': x['id'], 'url_small': x['small_url'], 'url_big': x['big_url']} for x in spisok
    ])

    if formset.is_valid():
        for form in formset:
            Pictures.objects.create(**form.cleaned_data)

    context['formset'] = formset
    return render(request, "new_photos.html", context)


def all_photos(request):
    data_list = []
    photo_list = list(Pictures.objects.all())
    context = {}
    GeeksFormSet = formset_factory(GeeksForm, extra=0)
    formset = GeeksFormSet(request.POST or None, initial=[
        {'id_photo': x.id_photo, 'url_small': x.url_small, 'url_big': x.url_big,
         'name': x.name, 'description': x.description,
         'visible': x.visible, 'not_upload': x.not_upload} for x in photo_list
    ])
    list_of_instance = []

    if formset.is_valid():
        for form in formset:
            for photo in photo_list:
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


    context['formset'] = formset
    return render(request, "all_photos.html", context)