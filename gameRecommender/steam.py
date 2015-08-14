import urllib2 as urllib
import json
import xml.etree.ElementTree as et
import BeautifulSoup as bs

from selenium import webdriver


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
            self.games.append(Game(i["appid"], i["img_icon_url"], i["name"], i["playtime_forever"]))

        return self.games

    def get_friends(self):
        url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=E770C55138B535447F8678136EFC9285&steamid=" + \
              self.name + "&relationship=friend"
        response = urllib.urlopen(url)
        data = json.loads(response.read())

        for i in data["friendslist"]["friends"]:
            self.friends.append(User(i["steamid"]))

        return self.friends

    def get_matching_games(self, users):

        games = self.games

        for i in users:
            if i.name != self.name:
                games = [x for x in games if x in i.games]

        return games

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
        self.image_url = image_url
        self.name = name
        self.playtime = int(playtime)

    def get_details(self):
        self._scrape_details()

    def _scrape_details(self):
        url = "http://store.steampowered.com/app/" + str(self.appid)

        # use driver to generate full HTML
        driver = webdriver.Firefox()
        driver.get(url)

        # bypass agecheck if necessary
        if "agecheck" in driver.current_url:
            driver.find_element_by_xpath("//select[@name='ageYear']/option[text()='1990']").click()
            driver.find_element_by_class_name("btnv6_blue_hoverfade").click()
        html = driver.page_source
        driver.close()

        # get tags
        soup = bs.BeautifulSoup(html)
        script_results = [i for i in soup('script', {'type': 'text/javascript'}) if "InitAppTagModal" in str(i)][0]
        tag_string = script_results.string
        tags = tag_string[tag_string.index("["):tag_string.index(",", tag_string.index("]"))]
        data = json.loads(tags)
        self.tags = [x["name"] for x in data]

        # get metascore
        result = soup.find("div", id="game_area_metascore").text
        score = result[:result.find("/")]
        try:
            int(score)
            self.metascore = score
        except ValueError:
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


if __name__ == "__main__":
    # tests go here
    game = User(76561198032447319).get_games()[0]
    game.get_details()

