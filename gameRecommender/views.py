from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import GameInfo
from .tables import GameTable


def index(request):
    game_list = GameTable(GameInfo.objects.all())
    RequestConfig(request).configure(game_list)
    context = {'game_list': game_list}
    return render(request, 'gameRecommender/index.html', context)
