

# Takes in a list of users and returns all games they have in common
# If a list of tags is passed in as the optional argument, it only returns games with those tags
def get_matching_games(*args, **kwargs):
    print [i for i in args]
    print [i for i in kwargs]
    tags = kwargs.pop("tags", None)

    print tags
    users = list(set(args))

    games = set(users[0].games)

    for i in users[1:]:
        gams = set(i.games)
        games = games.intersection(gams)

    if tags is None:
        return list(games)
    else:
        return [i for i in games if i.has_tags(tags)]
