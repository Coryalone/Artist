import re
import os

from django.http import HttpResponse
from django.shortcuts import render, redirect

import requests, json, time, random

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


def get_photos(request):
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


    return photos, fresh_photos


def sync(request):
    if request.method == 'POST':
        return redirect('photo')
    return render(request, 'sync.html')


def get_all_ids():
    check_list = list(Pictures.objects.values('id_photo'))
    pay_list = []
    for i in check_list:
        pay_list.append(i['id_photo'])
    return pay_list


def add_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)

    else:
        form = PostForm()
    return render(request, 'add_new.html', {'form': form})


# relative import of forms
from .forms import GeeksForm

# importing formset_factory
from django.forms import formset_factory


def formset_view(request):
    context = {}
    spisok = get_photos(request)[1]
    # creating a formset and 5 instances of GeeksForm
    GeeksFormSet = formset_factory(GeeksForm, extra=0)
    formset = GeeksFormSet(request.POST or None, initial=[
        {'id_photo': x['id'], 'url_small': x['small_url'], 'url_big': x['big_url']} for x in spisok
    ])

    # print formset data if it is valid
    if formset.is_valid():
        for form in formset:
            #print(form.cleaned_data)
            Pictures.objects.create(**form.cleaned_data)

    # Add the formset to context dictionary
    context['formset'] = formset
    #context['deep'] = [1, 2, 3]
    return render(request, "home.html", context)
