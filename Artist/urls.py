"""Artist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from main.admin_views import new_photos, all_photos
from main.front_views import api_shuffled_main_page_photos, api_photos_by_category, main_page, portraits, landscapes, \
    graphics, sculptures, murals, about

urlpatterns = [
    path('new_photos/', new_photos, name='new_photos'),
    path('admin/', all_photos, name='all_photos'),
    path('api/<int:category>', api_photos_by_category, name='api_category'),
    path('api/main_page', api_shuffled_main_page_photos, name='api_main_page'),
    path('', main_page, name='main_page'),
    path('portraits', portraits, name='portraits'),
    path('landscapes', landscapes, name='landscapes'),
    path('graphics', graphics, name='graphics'),
    path('sculptures', sculptures, name='sculptures'),
    path('murals', murals, name='murals'),
    path('about', about, name='about'),
    path("accounts/", include("django.contrib.auth.urls"))
]

