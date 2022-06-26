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

from main.views import sync, get_photos, add_new, formset_view, all_photos_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_photos/', get_photos, name='photo'),
    path('sync/', sync, name='sync'),
    path('add_new', add_new, name='add_new'),
    path('mult_forms', formset_view, name='formset_view'),
    path('all_photos_view', all_photos_view, name='all_photos_view'),
]
