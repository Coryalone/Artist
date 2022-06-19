from django.db import models


class Pictures(models.Model):
    id_photo = models.IntegerField()
    url_small = models.CharField(max_length=300, verbose_name='Урл маленькой фотографии')
    url_big = models.CharField(max_length=300, verbose_name='Урл большой фотографии')
    sync_date = models.DateTimeField(auto_now=True, verbose_name='Синхронизированно')
    name = models.CharField(max_length=50, verbose_name='Название картины', blank=True)
    description = models.CharField(max_length=150, verbose_name='Описание картины', blank=True)
    category = models.CharField(max_length=150, verbose_name='Наименование категории', blank=True)


