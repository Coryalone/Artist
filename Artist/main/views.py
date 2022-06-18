import re
import os

from django.http import HttpResponse
from django.shortcuts import render, redirect

import requests, json, time, random

from main.models import Pictures

VK_USER_ID = '62391816'
VK_TOKEN = os.environ['VK_TOKEN']


def sync_photos_data(offset=0, count=50):
    api = requests.get("https://api.vk.com/method/photos.getAll", params={
        'owner_id': VK_USER_ID,
        'access_token': VK_TOKEN,
        'offset': offset,
        'count': count,
        'photo_sizes': 0,
        'v': 5.103
    })
    return json.loads(api.text)


def sync_photos(request):
    urls_set = set()
    data = sync_photos_data()
    count_foto = data["response"]["count"] * 2  # TODO: сделать оптимизацию запросов
    i = 0
    count = 50
    while i <= count_foto:
        photos = sync_photos_data(offset=i, count=count)['response']['items']
        for lst in photos:
            for item in lst['sizes']:
                if item['type'] == 'm':
                    urls_set.add(item['url'])
                elif item['type'] == 'x':
                    urls_set.add(item['url'])
        i += count

    res = []
    clean_data = set()
    for suburl in urls_set:
        res.append(re.search(r"/[a-zA-Z0-9_\-]+\.(\w+)\?", suburl))

    for i in res:
        if i is not None:
            clean_data.add(i.group(0))

    if get_data():
        result = []
        filter_data = set()
        for suburl in get_data():
            result.append(re.search(r"/[a-zA-Z0-9_\-]+\.(\w+)\?", suburl))

        for i in result:
            if i is not None:
                filter_data.add(i.group(0))

        bd_data = list(filter_data)
        vk_api = list(clean_data)
        for url in vk_api:
            if url not in bd_data:
                pictures = Pictures(photos=url)
                pictures.save()

    else:
        for url in urls_set:
            pictures = Pictures(photos=url)
            pictures.save()


def sync(request):
    if request.method == 'POST':
        return redirect('photo')
    return render(request, 'sync.html')


def get_data():
    a = list(Pictures.objects.values('photos'))
    check_set = set()
    for i in a:
        check_set.add(i['photos'])
    return check_set
