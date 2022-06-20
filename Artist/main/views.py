import re
import os

from django.http import HttpResponse
from django.shortcuts import render, redirect

import requests, json, time, random

from main.models import Pictures

VK_USER_ID = '62391816'
VK_TOKEN = os.environ['VK_TOKEN']


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

    for photo in photos:
        if photo['id'] not in all_ids:
            pictures = Pictures(id_photo=photo['id'], url_small=photo['small_url'], url_big=photo['big_url'])
            pictures.save()

    return render(request,  'photos_list.html', {'news': photos})


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
