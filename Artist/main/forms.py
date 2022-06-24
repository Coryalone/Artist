from django import forms
from .models import Category

from django.forms import formset_factory


class PostForm(forms.Form):

    name = forms.CharField(max_length=150, widget=forms.TextInput(), initial='Breakfast')
    description = forms.CharField(widget=forms.Textarea())
    visible = forms.BooleanField()
    not_upload = forms.BooleanField()
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select())


class GeeksForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()
    id_photo = forms.IntegerField()
    url_small = forms.CharField()
    url_big = forms.CharField()


GeeksFormSet = formset_factory(GeeksForm)


