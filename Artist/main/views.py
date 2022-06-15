import re

from django.http import HttpResponse
from django.shortcuts import render, redirect

import requests, json, time, random

from main.models import Pictures

VK_USER_ID = '62391816'
VK_TOKEN = 'vk1.a.O8apl0KiwnzLmW7gcYU0DlVQZCyBRZ3HZAQx3gmktGjTI3ZcTx5CLPUEnf91njAzOxbTSLI-fIC9QSdv7SJ1ua9kqJZ7CzwJLf_X_Vl5p4DtpBAWC1mS_nbExvkMufhism26-wyUX8XaWF0rt5XZYo-GYTE2P9qHMB_fv6ZzuuGbhR69cbOrdHgd8oW25kMI'


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
    return HttpResponse("one<br>two<br>three<br>four<br>five<br>six<br>seven<br>")
    urls_set = set()
    data = get_foto_data()
    count_foto = data["response"]["count"] * 2  # сделать оптимизацию запросов
    # print(count_foto)
    photos = get_foto_data()['response']['items']
    i = 0
    w = 0
    count = 50
    fotos = []
    while i <= count_foto:
        if i != 0:
            # print(i)
            photos = get_foto_data(offset=i, count=count)['response']['items']
        # print(len(photos))
        for lst in photos:
            for item in lst['sizes']:
                if item['type'] == 'm':
                    urls_set.add(item['url'])
                    fotos.append(item['url'])
                    # print(item['url'])
                elif item['type'] == 'x':
                    urls_set.add(item['url'])
                    fotos.append(item['url'])
        # print(i)
        i += count
        # w += len(urls_set)

    # print(len(fotos))
    # print(str(len(urls_set))+' длинна')
    # print(len(get_data()))
    # print(len(urls_set))
    # print(get_data())
    res = []
    clean_data = set()
    for suburl in urls_set:
        res.append(re.search(r"/[a-zA-Z0-9_\-]+\.(\w+)\?", suburl))

    for i in res:
        if i is not None:
            clean_data.add(i.group(0))

    # pes = (get_data().difference_update(urls_set))
    # print(pes)
    counter = 0
    if get_data():
        result = []
        filter_data = set()
        for suburl in get_data():
            result.append(re.search(r"/[a-zA-Z0-9_\-]+\.(\w+)\?", suburl))

        for i in result:
            if i is not None:
                filter_data.add(i.group(0))

        bd_data = list(filter_data)
        #print(qer)
        vk_api = list(clean_data)
        #print(qer == wer)
        ZALUPA = 0
        for url in vk_api:
            if url not in bd_data:
                pictures = Pictures(photos=url)
                pictures.save()
            else:
                pass
        print(ZALUPA)

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
