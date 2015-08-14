__author__ = 'Dean'

from gameRecommender.models import GameInfo


def game_in_db(game_id):

    if GameInfo.objects.filter(app_ID=game_id):
        return True
    else:
        return False
