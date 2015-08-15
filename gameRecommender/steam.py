import urllib2 as urllib
import json
import xml.etree.ElementTree as et
import BeautifulSoup as bs

import django
import dryscrape

import crud


class User:

    def __init__(self, name):
        # check if username or ID
        self.name = self._get_id(str(name))

        self.games = []
        self.friends = []

    def get_games(self):
        url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=E770C55138B535447F8678136EFC9285&steamid=" + \
            self.name + "&format=json&include_played_free_games=1&include_appinfo=1"
        response = urllib.urlopen(url)
        data = json.loads(response.read())

        for i in data["response"]["games"]:
            self.games.append(Game(i["appid"], i["img_logo_url"], i["name"], i["playtime_forever"]))

        return self.games

    def get_friends(self):
        url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=E770C55138B535447F8678136EFC9285&steamid=" + \
              self.name + "&relationship=friend"
        response = urllib.urlopen(url)
        data = json.loads(response.read())

        for i in data["friendslist"]["friends"]:
            self.friends.append(User(i["steamid"]))

        return self.friends

    def get_matching_games(self, users, tags=None):

        games = self.games

        for i in users:
            if i.name != self.name:
                games = [x for x in games if x in i.games]

        if tags is None:
            return games
        else:
            return [i for i in games if i.has_tags(tags)]

    def get_games_with_tags(self, tags):
        return [i for i in self.games if i.has_tags(tags)]

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
        self.appid = int(appid)
        self.image_url = \
            "http://media.steampowered.com/steamcommunity/public/images/apps/" + str(appid) + \
            "/" + image_url + ".jpg"
        self.name = name
        self.playtime = int(playtime)

        # initialise to None in case game does not exist
        self.tags = None
        self.metascore = None
        self.positive_reviews = None
        self.negative_reviews = None
        self.features = None

        if not crud.game_in_db(self.appid):
            self._get_details()
            crud.add_game_db(self)
        else:
            game_info = crud.get_game_info(appid)
            self.tags = [i["tags"] for i in game_info.gameTags.filter().values("tags")]
            self.metascore = game_info.metascore
            self.positive_reviews = game_info.positive_review_numbers
            self.negative_reviews = game_info.negative_review_numbers
            self.features = [i["features"] for i in game_info.gameFeatures.filter().values("features")]

    def _get_details(self):
        self._scrape_details()

    def _scrape_details(self):
        url = "http://store.steampowered.com/app/" + str(self.appid)

        # use driver to generate full HTML
        sess = dryscrape.Session()
        sess.visit(url)

        # make sure game exists
        if sess.url() == "http://store.steampowered.com/":
            return

        # bypass agecheck if necessary
        if "agecheck" in sess.url():
            q = sess.at_xpath('//*[@name="ageYear"]')
            q.set("1990")
            q.form().submit()

        # get tags
        soup = bs.BeautifulSoup(sess.body())
        script_results = [i for i in soup('script', {'type': 'text/javascript'}) if "InitAppTagModal" in str(i)][0]
        tag_string = script_results.string
        tags = tag_string[tag_string.index("["):tag_string.index(",", tag_string.index("]"))]
        data = json.loads(tags)
        self.tags = [x["name"] for x in data]

        # get metascore
        try:
            result = soup.find("div", id="game_area_metascore").text
            score = result[:result.find("/")]
            int(score)
            self.metascore = score
        except (ValueError, AttributeError):
            self.metascore = None

        # get review count
        votes = str(soup.find(id="ReviewsTab_positive"))
        positive = votes[votes.find('t">')+4:votes.find(")</")]
        votes = str(soup.find(id="ReviewsTab_negative"))
        negative = votes[votes.find('t">')+4:votes.find(")</")]
        self.positive_reviews = int(positive.replace(",", ""))
        self.negative_reviews = int(negative.replace(",", ""))

        # get features
        result2 = soup.findAll("a", {"class": "name"})
        self.features = [i.string for i in result2]

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

    def has_tags(self, tags):
        for i in tags:
            if i not in self.tags:
                return False
        return True


if __name__ == "__main__":
    # tests go here
    django.setup()
    game = User(76561198189868938).get_games()[1]
    game.print_game()
