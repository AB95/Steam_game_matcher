__author__ = 'Dean'

from gameRecommender.models import GameInfo, GameTags, GameFeatures


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


def get_tag(tag_check):

    if check_tag(tag_check):
        tag = GameTags.objects.get(tags=tag_check)
        return tag
    else:
        return "no tag found"


def get_feature(feature_check):

    if check_feature(feature_check):
        feature = GameFeatures.objects.get(features=feature_check)
        return feature
    else:
        return "no feature found"


def add_game_db(game_object):

    if game_in_db(game_object.appid):

        return "game is already in the DB"

    elif game_object.tags is None and game_object is None:

        return "game has no tags or features"

    else:

        new_game = GameInfo(game_name=game_object.name, app_ID=game_object.appid, metascore=game_object.metascore,
                            positive_review_numbers=game_object.positive_reviews,
                            negative_review_numbers=game_object.negative_reviews,
                            picture=game_object.image_url,)
        new_game.save()

        if game_object.tags:
            for item in game_object.tags:
                if not check_tag(item):
                    add_tag(item)
                    new_game.gameTags.add(get_tag(item))
                else:
                    new_game.gameTags.add(get_tag(item))

        if game_object.features:
            for item in game_object.features:
                if not check_feature(item):
                    add_feature(item)
                    new_game.gameFeatures.add(get_feature(item))
                else:
                    new_game.gameFeatures.add(get_feature(item))

        new_game.save()


def check_tag(tag):

    if GameTags.objects.filter(tags=tag):
        return True
    else:
        return False


def check_feature(feature):

    if GameFeatures.objects.filter(features=feature):
        return True
    else:
        return False


def add_tag(tag):

    new_tag = GameTags.objects.create(tags=tag)
    new_tag.save()


def add_feature(feature):

    new_feature = GameFeatures.objects.create(features=feature)
    new_feature.save()
