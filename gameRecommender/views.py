from django.shortcuts import render
from django_tables2 import RequestConfig
from errors import ProfileNotFoundException
import user
import utils
from .models import GameInfo
from .tables import GameTable
from .forms import UserIDForm, TagForm


# TODO show errors for incorrect user names/ids and clean up


def index(request):
    request.session.set_expiry(5)
    user_list = []
    tags = []
    if request.method == 'POST':
        form = UserIDForm(request.POST)
        if form.is_valid():
            user_id_1 = request.POST['user_ID_1']
            user_id_2 = request.POST['user_ID_2']
            tags = request.POST.getlist('tags')
            request.session['tags'] = tags
            try:
                user_list = [user.User(user_id_1), user.User(user_id_2)]
                request.session['user_list'] = user_list
            except ProfileNotFoundException:
                try:
                    user_list = request.session['user_list']
                except KeyError:
                    user_list = []

    else:
        try:
            user_list = request.session['user_list']
            tags = request.session['tags']
        except KeyError:
            pass

    tag_form = TagForm()
    user_form = UserIDForm()
    table = make_table(user_list, tags)
    RequestConfig(request).configure(table)
    context = {'game_list': table, 'user_form': user_form, 'tag_form': tag_form}
    return render(request, 'gameRecommender/index.html', context)


def make_table(list_users, tags):

    if list_users:
        game_list = utils.get_matching_games(list_users)
        if tags:
            game_list = utils.filter_by_tags(game_list, tags)
        table = GameTable(game_list)
    else:
        table = GameTable(GameInfo.objects.all())

    return table
