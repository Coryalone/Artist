from django.db import models


class Pictures(models.Model):
    id_photo = models.IntegerField()
    url_small = models.CharField(max_length=300, verbose_name='Урл маленькой фотографии')
    url_big = models.CharField(max_length=300, verbose_name='Урл большой фотографии')
    sync_date = models.DateTimeField(auto_now=True, verbose_name='Синхронизированно')
    name = models.CharField(max_length=50, verbose_name='Название картины', blank=True)
    description = models.CharField(max_length=150, verbose_name='Описание картины', blank=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, blank=True)
    visible = models.BooleanField(default=False, verbose_name='Отображать на главной', blank=True, null=True)
    not_upload = models.BooleanField(default=False, verbose_name='Не загружать из ВК', blank=True, null=True)




class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование категории')

    def __str__(self):
        return self.title


