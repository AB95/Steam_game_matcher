__author__ = 'Dean'

import django_tables2 as tables
from gameRecommender.models import GameInfo


class GameTable(tables.Table):

    game_tags_column = tables.Column(empty_values=(), accessor='gameTags', orderable=False, verbose_name='Game Tags')
    game_features_column = tables.Column(empty_values=(), accessor='gameFeatures', orderable=False,
                                         verbose_name='Game Features')
    operating_systems_column = tables.Column(accessor='operating_systems', orderable=False)
    name_column = tables.TemplateColumn('<a href="{{record.store_url}}">{{record.name}}</a>', verbose_name='Name',
                                        accessor='name')

    def render_operating_systems_column(self, value):

        data = ''
        operating_systems = value

        for item in operating_systems:
            data += item + ' '

        return data

    def render_game_tags_column(self, record):

        data = ''
        tags = record.gameTags.filter().values('tags')

        for item in tags:
            data += item['tags'] + ' '

        return data

    def render_game_features_column(self, record):

        data = ''
        features = record.gameFeatures.filter().values('features')

        for item in features:
            data += item['features'] + ' '

        return data

    class Meta:
        model = GameInfo
        fields = ('app_id', 'metascore', 'positive_reviews', 'negative_reviews')
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        order_by = 'app_id'
        sequence = ('name_column', '...')
