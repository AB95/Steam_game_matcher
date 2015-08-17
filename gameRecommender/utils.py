

# Takes in a list of users and returns all games they have in common
# If a list of tags is passed in as the optional argument, it only returns games with those tags
def get_matching_games(users, tags=None):
    users = set(users)

    games = users[0].games.keys()

    for i in users:
        games = [x for x in games if x in i.games.keys()]

    if tags is None:
        return games
    else:
        return [i for i in games if i.has_tags(tags)]