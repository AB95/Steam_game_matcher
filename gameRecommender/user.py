import urllib2 as urllib
import json
import xml.etree.ElementTree as et

from errors import ProfileNotFoundException
from game import Game


class User:

    def __init__(self, name):
        # check if username or ID
        self.name = self._get_id(str(name))
        self.games_total = 0
        self.games = {}
        self.friends = []
        self.get_games()

    def get_games(self):
        # Construct URL for the api then grab the json
        url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=E770C55138B535447F8678136EFC9285&steamid=" + \
            self.name + "&format=json&include_played_free_games=1&include_appinfo=1"

        try:
            response = urllib.urlopen(url)
        except urllib.HTTPError:
            print "Games could not be fetched due to", response.getcode(), "error"
            return

        data = json.loads(response.read())

        if data["response"] == {}:
            print "Games could not be fetched due to false response"
            return

        self.games_total = data["response"]["game_count"]

        games_list = data["response"]["games"]

        # from gameRecommender import crud

        # self.games = [crud.get_game_info(i["appid"]) for i in games_list]

        # Parse the json, turn it into a Game object and add it to the user's game list
        # TODO: Change from indexing to pythonic for loop
        for i in xrange(len(games_list)):
            print str(i+1) + "/" + str(self.games_total)
            self.games[(Game(games_list[i]["appid"], games_list[i]["img_logo_url"], games_list[i]["name"]))] = int(games_list[i]["playtime_forever"])

        return self.games

    # Grabs the user's friends list in the form of their Steam id's
    def get_friends(self):
        url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=E770C55138B535447F8678136EFC9285&steamid=" + \
              self.name + "&relationship=friend"
        response = urllib.urlopen(url)
        data = json.loads(response.read())

        for i in data["friendslist"]["friends"]:
            self.friends.append(User(i["steamid"]))

        return self.friends

    # Takes in a list of tags and returns only games the user owns with those tags
    def get_games_with_tags(self, tags):
        return [i for i in self.games.keys() if i.has_tags(tags)]

    # Determines whether the user's ID or vanity URL was passed in and fetches the ID if it was a vanity URL
    def _get_id(self, username):
        try:
            assert len(username) >= 16
            int(username)
            return username
        except (AssertionError, ValueError):
            if "steamcommunity.com" in username:
                url = username
                if "www." not in username:
                    url = "www." + url
                if "http://" not in username:
                    url = "http://" + url
                if "?xml=1" not in username:
                    url += "?xml=1"
            else:
                url = "http://www.steamcommunity.com/id/" + username + "?xml=1"
            response = urllib.urlopen(url)
            tree = et.parse(response)
            root = tree.getroot()
            text = root[0].text
            if text == "The specified profile could not be found.":
                raise ProfileNotFoundException(username)
            else:
                return text
