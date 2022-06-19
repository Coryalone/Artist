import re

from django.http import HttpResponse
from django.shortcuts import render, redirect

import requests, json, time, random

from main.models import Pictures

VK_USER_ID = '62391816'
VK_TOKEN = 'vk1.a.Dmkh1g3hhOi7hEGyDOtv4Ft6evuFAvdgoA1UywVZR1aGFrysnXE1RR27PNoM6g26zLH6gfKO7HIYj6F3R0wGHnKUkGBS3ET-Hdg78SNWgl4aubWxQ0W1BX4YIjYvzlQuTjAKrwKIQQnOJE6ZOvbNUpffsaF2huGvmVS98b0eSPQuPDfLcDAxp38rsK6Mw-KT'


def get_foto_data(offset=0, count=50):
    api = requests.get("https://api.vk.com/method/photos.getAll", params={
        'owner_id': VK_USER_ID,
        'access_token': VK_TOKEN,
        'offset': offset,
        'count': count,
        'photo_sizes': 0,
        'v': 5.103
    })
    return json.loads(api.text)


def get_foto(request):

    urls_set = set()

    photo_url = []

    data = get_foto_data()
    count_foto = data["response"]["count"]   # сделать оптимизацию запросов
    # print(count_foto)
    photos = get_foto_data()['response']['items']
    id_shit = [x['id'] for x in photos]
    #print(id_shit)
    i = 0
    w = 0
    count = 50
    fotos = []
    while i <= count_foto:
        if i != 0:
            # print(i)
            photos = get_foto_data(offset=i, count=count)['response']['items']
        # print(len(photos))
        for dick in photos:
            new_photo = {}

            new_photo['id'] = dick['id']
            for item in dick['sizes']:
                if item['type'] == 'm':
                    new_photo['small_url'] = item['url']
                elif item['type'] == 'x':
                    new_photo['big_url'] = item['url']

            photo_url.append(new_photo)

        # print(i)
        i += count
        # w += len(urls_set)

    # print(len(fotos))
    #print(photo_url)
    # print(str(len(urls_set))+' длинна')
    # print(len(get_data()))
    #print((urls_set))
    # print(get_data())

    all_ids = get_data()

    for photo in photo_url:
        if photo['id'] not in all_ids:
            pictures = Pictures(id_photo=photo['id'], url_small=photo['small_url'], url_big=photo['big_url'])
            pictures.save()

    return render(request,  'photos_list.html', {'news': photo_url})


def sync(request):
    if request.method == 'POST':
        return redirect('photo')
    return render(request, 'sync.html')


def get_data():
    check_list = list(Pictures.objects.values('id_photo'))
    pay_list = []
    for i in check_list:
        pay_list.append(i['id_photo'])
    return pay_list
