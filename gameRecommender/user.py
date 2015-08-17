import urllib2 as urllib
import json
import xml.etree.ElementTree as et

from game import Game


class User:

    def __init__(self, name):
        # check if username or ID
        self.name = self._get_id(str(name))
        self.games_total = 0
        self.games = {}
        self.friends = []

    def get_games(self):
        # Construct URL for the api then grab the json
        url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=E770C55138B535447F8678136EFC9285&steamid=" + \
            self.name + "&format=json&include_played_free_games=1&include_appinfo=1"
        response = urllib.urlopen(url)
        data = json.loads(response.read())

        self.games_total = data["response"]["game_count"]

        # Parse the json, turn it into a Game object and add it to the user's game list
        for i in data["response"]["games"]:
            self.games[(Game(i["appid"], i["img_logo_url"], i["name"]))] = int(i["playtime_forever"])

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

    # Takes in a list of users and returns all games they have in common
    # If a list of tags is passed in as the optional argument, it only returns games with those tags
    def get_matching_games(self, users, tags=None):

        games = self.games.keys()

        for i in users:
            if i.name != self.name:
                games = [x for x in games if x in i.games.keys()]

        if tags is None:
            return games
        else:
            return [i for i in games if i.has_tags(tags)]

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
                raise Exception("Profile not found")
            else:
                return text