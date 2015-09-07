import urllib2 as urllib
import json
import xml.etree.ElementTree as et
from game import Game

from gameRecommender import crud
from errors import ProfileNotFoundException, InvalidInputException
from socket import timeout


class User:

    def __init__(self, name):
        # check if username or ID
        self.name = self._get_id(str(name))
        self.games_total = 0
        self.games = {}
        self._games_list = []
        self.friends = []
        self.get_games()

    def get_games(self):
        # Construct URL for the api then grab the json

        with open("gameRecommender/key.txt", "r") as f:
            key = f.read()

        url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + key + "&steamid=" + \
            self.name + "&format=json&include_played_free_games=1&include_appinfo=1"

        # TODO: Throw specific exceptions for this
        try:
            response = urllib.urlopen(url, timeout=20)
        except urllib.HTTPError:
            print "Games could not be fetched due to", response.getcode(), "error"
            return
        except timeout:
            print "Games could not be fetched due to timeout"
            return

        data = json.loads(response.read())

        if data["response"] == {}:
            print "Games could not be fetched due to false response"
            return

        self.games_total = data["response"]["game_count"]

        self._games_list = data["response"]["games"]

        played_times = [i["playtime_forever"] for i in self._games_list]

        # Parse the json, turn it into a Game object and add it to the user's game list
        # self.games = {crud.get_game_info(i["appid"]): i["playtime_forever"] for i in games_list}
        self.games = dict(zip(crud.get_all_games({i["appid"] for i in self._games_list}), played_times))

        # Old way to do it, kept in case of things breaking
        # self.games = {Game(i["appid"], i["img_logo_url"], i["name"]): i["playtime_forever"] for i in games_list}

        return self.games

    # Grabs new game data from the internet rather than from the database
    def update_games(self):
        self.games = {Game(i["appid"], i["img_logo_url"], i["name"]): i["playtime_forever"] for i in self._games_list}
        return self.games

    # Grabs the user's friends list in the form of their Steam id's
    def get_friends(self):

        with open("key.txt", "r") as f:
            key = f.read()

        url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=" + key + "&steamid=" + \
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
    # Uses broad exception clauses as any input that does not work here is invalid
    def _get_id(self, username):
        try:
            assert len(username) >= 16
            int(username)
            return username
        except:
            try:
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
            except:
                raise InvalidInputException(username)
