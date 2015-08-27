from django.shortcuts import render
from django_tables2 import RequestConfig
from errors import ProfileNotFoundException
import user
import utils
from .models import GameInfo
from .tables import GameTable
from .forms import UserIDForm, TagForm, FeaturesForm, OSForm


# TODO show errors for incorrect user names/ids and clean up


def index(request):
    request.session.set_expiry(60)
    user_list = []
    tags = []
    features = []
    operating_systems = []

    if request.method == 'POST':
        form = UserIDForm(request.POST)

        if form.is_valid():
            user_id_1 = request.POST['user_ID_1']
            user_id_2 = request.POST['user_ID_2']
            tags = request.POST.getlist('tags')
            features = request.POST.getlist('features')
            operating_systems = request.POST.getlist('operating_systems')
            request.session['tags'] = tags
            request.session['features'] = features
            request.session['operating_systems'] = operating_systems

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
            features = request.session['features']
            operating_systems = request.session['operating_systems']
        except KeyError:
            pass

    features_form = FeaturesForm()
    tag_form = TagForm()
    user_form = UserIDForm()
    operating_systems_form = OSForm()
    table = make_table(user_list, tags, features, operating_systems)
    RequestConfig(request).configure(table)
    context = {'game_list': table, 'user_form': user_form, 'tag_form': tag_form, 'features_form': features_form,
               'operating_systems_form': operating_systems_form}
    return render(request, 'gameRecommender/index.html', context)


def make_table(list_users, tags, features, operating_systems):

    if list_users:
        game_list = utils.get_matching_games(list_users)

        if tags:
            game_list = utils.filter_by_tags(game_list, tags)

        if features:
            game_list = utils.filter_by_features(game_list, features)

        if operating_systems:
            game_list = utils.filter_by_os(game_list, operating_systems)

        table = GameTable(game_list)
    else:
        table = GameTable(GameInfo.objects.all())

    return table
