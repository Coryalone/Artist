from django.db import models


class Pictures(models.Model):
    photos = models.CharField(max_length=200, verbose_name='Урл фотографии')
    sync_date = models.DateTimeField(auto_now=True, verbose_name='Синхронизированно')
    name = models.CharField(max_length=50, verbose_name='Название картины', blank=True)
    description = models.CharField(max_length=150, verbose_name='Описание картины', blank=True)
    category = models.CharField(max_length=150, verbose_name='Наименование категории', blank=True)


