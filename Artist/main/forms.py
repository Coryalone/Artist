from django import forms
from .models import Category

from django.forms import formset_factory


class PicturesForm(forms.Form):
    name = forms.CharField(required=False, label='Название')
    description = forms.CharField(required=False, label='Описание', widget=forms.Textarea())
    id_photo = forms.IntegerField()
    url_small = forms.CharField()
    url_big = forms.CharField()
    visible = forms.BooleanField(required=False, label='Отображать на главной стр.')
    not_upload = forms.BooleanField(required=False, label='Не загружать из ВК на сайт')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(), initial=6,
                                      label='Категория')





