from gameRecommender import crud


# Takes in a list of users and returns all games they have in common
# If a list of tags is passed in as the optional argument, it only returns games with those tags
def get_matching_games(users):
    games = set(users[0].games)

    for i in users[1:]:
        gams = set(i.games)
        games = games.intersection(gams)

    return games


def filter_by_tags(games, tags):
    return set(games).intersection(crud.get_all_games_by_tag(tags))


def filter_by_features(games, features):
    return set(games).intersection(crud.get_all_games_by_feature(features))


def filter_by_os(games, os):
    return set(games).intersection(crud.get_all_games_by_os(os))