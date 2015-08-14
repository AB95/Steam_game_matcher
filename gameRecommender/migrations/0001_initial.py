# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GameFeatures',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('features', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='GameInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_name', models.CharField(max_length=255)),
                ('app_ID', models.PositiveIntegerField()),
                ('metascore', models.PositiveIntegerField()),
                ('positive_review_numbers', models.PositiveIntegerField()),
                ('negative_review_numbers', models.PositiveIntegerField()),
                ('picture', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='GameTags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags', models.CharField(max_length=255)),
                ('gameInfo', models.ManyToManyField(to='gameRecommender.GameInfo')),
            ],
        ),
        migrations.AddField(
            model_name='gamefeatures',
            name='gameInfo',
            field=models.ManyToManyField(to='gameRecommender.GameInfo'),
        ),
    ]
