__author__ = 'Dean'

from gameRecommender.models import GameInfo


def game_in_db(game_id):

    if GameInfo.objects.filter(app_ID=game_id):
        return True
    else:
        return False


def get_game_info(game_id):

    if game_in_db(game_id):

        game = GameInfo.objects.get(app_ID=game_id)
        return game

    else:
        return "Game is not in the database"
