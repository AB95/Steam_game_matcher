

# Takes in a list of users and returns all games they have in common
# If a list of tags is passed in as the optional argument, it only returns games with those tags
def get_matching_games(users):
    games = set(users[0].games)

    for i in users[1:]:
        gams = set(i.games)
        games = games.intersection(gams)

    return games


def filter_by_tags(games, tags):
    return {i for i in games if has_tags(i, tags)}


def filter_by_features(games, features):
    return {i for i in games if has_features(i, features)}


def has_tags(game, tags):
    game_tags = {i["tags"] for i in game.gameTags.filter().values("tags")}
    if type(tags) == list:
        for i in tags:
            if i not in game_tags:
                return False
        return True
    else:
        return tags in game_tags


def has_features(game, features):
    game_features = {i["features"] for i in game.gameFeatures.filter().values("features")}
    if type(features) == list:
        for i in features:
            if i not in game_features:
                return False
        return True
    else:
        return features in game_features