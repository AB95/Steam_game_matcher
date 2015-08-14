# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameRecommender', '0002_auto_20150807_1942'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gameinfo',
            options={'ordering': ('app_ID',)},
        ),
        migrations.AlterField(
            model_name='gamefeatures',
            name='features',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='gameinfo',
            name='app_ID',
            field=models.PositiveIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='gameinfo',
            name='metascore',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='gametags',
            name='tags',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
