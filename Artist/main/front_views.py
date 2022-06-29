import random

from django.http import JsonResponse

from main.models import Pictures


def api_photos_by_category(request):
    category = request.GET.get('n', '')
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



