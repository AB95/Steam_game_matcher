import urllib2 as urllib
import json
import xml.etree.ElementTree as ET


def _getOwnedGamesByUserID(userID, includeFree):
    url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=E770C55138B535447F8678136EFC9285&steamid=" + \
          userID + "&format=json&include_played_free_games=" + str(includeFree) + "&include_appinfo=1"
    response = urllib.urlopen(url)
    data = json.loads(response.read())

    games = []

    for i in data["response"]["games"]:
        games.append(i["name"])

    return games


def _getID(username):
    url = "http://www.steamcommunity.com/id/" + username + "?xml=1"
    response = urllib.urlopen(url)
    tree = ET.parse(response)
    root = tree.getroot()
    return root[0].text


def getOwnedGames(user, includeFree=0):
    try:
        return _getOwnedGamesByUserID(user, includeFree)
    except urllib.HTTPError:
        return _getOwnedGamesByUserID(_getID(user), includeFree)


def getMatchingGames(users, includeFree=0):
    if len(users) > 1:
        games = getOwnedGames(users[0])

        for i in xrange(1, len(users)):
            gamesList = getOwnedGames(users[i])
            print len(gamesList), users[i]
            games = [x for x in games if x in gamesList]

        print "---------------------"
        return games

    elif len(users) == 1:
        return getOwnedGames(users[0])


# print getOwnedGames("76561198032447319")
games = getMatchingGames(["alexishbob2", "q1w2e3286"])

games.sort()

for i in games:
    print i