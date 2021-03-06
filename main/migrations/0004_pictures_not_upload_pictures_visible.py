# Generated by Django 4.0 on 2022-06-20 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_pictures_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='pictures',
            name='not_upload',
            field=models.BooleanField(default=False, verbose_name='Не загружать из ВК'),
        ),
        migrations.AddField(
            model_name='pictures',
            name='visible',
            field=models.BooleanField(default=False, verbose_name='Отображать на главной'),
        ),
    ]
