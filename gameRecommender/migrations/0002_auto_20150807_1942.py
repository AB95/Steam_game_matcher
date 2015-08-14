# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameRecommender', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamefeatures',
            name='gameInfo',
        ),
        migrations.RemoveField(
            model_name='gametags',
            name='gameInfo',
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='gameFeatures',
            field=models.ManyToManyField(to='gameRecommender.GameFeatures'),
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='gameTags',
            field=models.ManyToManyField(to='gameRecommender.GameTags'),
        ),
    ]
