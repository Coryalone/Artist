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
from django.urls import path

from main.admin_views import new_photos, all_photos
from main.front_views import api_shuffled_main_page_photos, api_photos_by_category

urlpatterns = [
    path('new_photos/', new_photos, name='new_photos'),
    path('admin/', all_photos, name='all_photos'),
    path('api/category', api_photos_by_category, name='api_category'),
    path('api/main_page', api_shuffled_main_page_photos, name='api_main_page'),
]

