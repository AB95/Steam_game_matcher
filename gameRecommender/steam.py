import urllib2 as urllib
import json
import xml.etree.ElementTree as et
import BeautifulSoup as bs

import django
import mechanize

import crud
import errors


class User:

    def __init__(self, name):
        # check if username or ID
        self.name = self._get_id(str(name))

        self.games_total = 0
        self.games = []
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
            self.games.append(Game(i["appid"], i["img_logo_url"], i["name"], i["playtime_forever"]))

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

        games = self.games

        for i in users:
            if i.name != self.name:
                games = [x for x in games if x in i.games]

        if tags is None:
            return games
        else:
            return [i for i in games if i.has_tags(tags)]

    # Takes in a list of tags and returns only games the user owns with those tags
    def get_games_with_tags(self, tags):
        return [i for i in self.games if i.has_tags(tags)]

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


class Game:

    def __init__(self, appid, image_url, name, playtime):
        # Initialise known values
        self.appid = int(appid)
        self.image_url = \
            "http://media.steampowered.com/steamcommunity/public/images/apps/" + str(appid) + \
            "/" + image_url + ".jpg"
        self.name = name
        self.playtime = int(playtime)

        # Initialise to None in case game does not exist
        self.tags = None
        self.metascore = None
        self.positive_reviews = None
        self.negative_reviews = None
        self.features = None
        self.store_url = None

        self._get_details()

    # Checks if game is in the database, otherwise scrapes the web for the data
    def _get_details(self):
        if not crud.game_in_db(self.appid):
            self._get_details()
            crud.add_game_db(self)
        else:
            game_info = crud.get_game_info(self.appid)
            self.tags = [i["tags"] for i in game_info.gameTags.filter().values("tags")]
            self.metascore = game_info.metascore
            self.positive_reviews = game_info.positive_review_numbers
            self.negative_reviews = game_info.negative_review_numbers
            self.features = [i["features"] for i in game_info.gameFeatures.filter().values("features")]

    # Scrapes info from the game's site
    def _scrape_details(self):
        url = "http://store.steampowered.com/app/" + str(self.appid)

        # Use driver to generate full HTML
        br = mechanize.Browser()
        response = br.open(url)

        # Make sure game exists
        if response.geturl() == "http://store.steampowered.com/":
            return

        # Bypass agecheck if necessary
        if "agecheck" in response.geturl():
            br.form = list(br.forms())[1]
            control = br.form.controls[3]
            control.value = ["1990"]
            response = br.submit()

        # Parses the html using BeautifulSoup
        soup = bs.BeautifulSoup(response.read())

        # Simple returns if a site error occurs
        if soup.title.string == "Site Error":
            return

        try:
            # Get tags
            script_results = [i for i in soup('script', {'type': 'text/javascript'}) if "InitAppTagModal" in str(i)][0]
            tag_string = script_results.string
            tags = tag_string[tag_string.index("["):tag_string.index(",", tag_string.index("]"))]
            data = json.loads(tags)
            self.tags = [x["name"] for x in data]

            # Get review count
            votes = str(soup.find(id="ReviewsTab_positive"))
            positive = votes[votes.find('t">')+4:votes.find(")</")]
            votes = str(soup.find(id="ReviewsTab_negative"))
            negative = votes[votes.find('t">')+4:votes.find(")</")]
            self.positive_reviews = int(positive.replace(",", ""))
            self.negative_reviews = int(negative.replace(",", ""))

            # Get features
            result2 = soup.findAll("a", {"class": "name"})
            self.features = [i.string for i in result2]
        # Shows the game has no tags and therefore an error has occurred
        except IndexError:
            pass
        # Can occur with more than one user tries to access the database at once
        except errors.AlreadyInDatabaseException:
            self._get_details()

        # Get metascore
        try:
            result = soup.find("div", id="game_area_metascore").text
            score = result[:result.find("/")]
            int(score)
            self.metascore = score
        # Games without a metascore are labelled "N/A" on the site
        except (ValueError, AttributeError):
            self.metascore = None

        # Down here so that if the store page doesn't exist, is set to None
        self.store_url = url

    def print_game(self):
        print "appid:", self.appid
        print "image URL:", self.image_url
        print "name:", self.name
        print "playtime:", self.playtime
        print "tags:", self.tags
        print "metascore:", self.metascore
        print "positive review count:", self.positive_reviews
        print "negative review count:", self.negative_reviews
        print "features:", self.features

    # Made above list comprehensions easier to reason
    def has_tags(self, tags):
        for i in tags:
            if i not in self.tags:
                return False
        return True


if __name__ == "__main__":
    # tests go here
    django.setup()
    user = User(76561198021143995)
    games_list = user.get_games()

    # 76561198032447319 Bouch
    # 76561198021143995 Matt
    # 76561198018709098 Dan
    # 76561198189868938 Squacks

    # people with most games on Steam:
    # 76561198000611224 76561198017902347 76561197971026489 76561197981142609 76561198026221141
