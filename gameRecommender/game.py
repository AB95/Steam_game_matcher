import BeautifulSoup as bs
import json

# Needed for a mechanize exception only
import urllib2

import mechanize

import crud
import errors


class Game:

    def __init__(self, app_id, image_url, name):
        # Initialise known values
        self.app_id = int(app_id)
        self.image_url = \
            "http://media.steampowered.com/steamcommunity/public/images/apps/" + str(app_id) + \
            "/" + image_url + ".jpg"
        self.name = name

        # Initialise to None in case game does not exist
        self.tags = None
        self.metascore = None
        self.positive_reviews = None
        self.negative_reviews = None
        self.features = None
        self.store_url = None
        self.operating_systems = []

        self._get_details()

    def __eq__(self, other):
        return self.app_id == other.app_id

    def __hash__(self):
        return hash(self.app_id)

    # Checks if game is in the database, otherwise scrapes the web for the data
    # If the page cannot be loaded for some reason, the game is not stored in the database
    def _get_details(self):

        try:
            game_info = crud.get_game_info(self.app_id)
            self.tags = [i["tags"] for i in game_info.gameTags.filter().values("tags")]
            self.metascore = game_info.metascore
            self.positive_reviews = game_info.positive_reviews
            self.negative_reviews = game_info.negative_reviews
            self.features = [i["features"] for i in game_info.gameFeatures.filter().values("features")]
            self.store_url = game_info.store_url
            self.operating_systems = game_info.operating_systems
        except errors.NotInDatabaseException:
            try:
                self._scrape_details()
                crud.add_game_db(self)
            except errors.PageNotLoadedException:
                return

    # Scrapes info from the game's site
    def _scrape_details(self, repeat=False):

        # TODO: Handle timeouts etc.

        url = "http://store.steampowered.com/app/" + str(self.app_id)

        # Use driver to generate full HTML
        br = mechanize.Browser()

        try:
            response = br.open(url)
        except urllib2.HTTPError:
            if not repeat:
                self._scrape_details(repeat=True)
            else:
                br.close()
                raise errors.PageNotLoadedException(self.app_id)

        # Make sure game exists
        if response.geturl() == "http://store.steampowered.com/":
            response.close()
            br.clear_history()
            br.close()
            return

        # Bypass agecheck if necessary
        if "agecheck" in response.geturl():
            br.form = list(br.forms())[1]
            control = br.form.controls[3]
            control.value = ["1990"]
            response = br.submit()

        # Parses the html using BeautifulSoup
        soup = bs.BeautifulSoup(response.read())

        response.close()
        br.clear_history()

        # Simple returns if a site error occurs
        if soup.title.string == "Site Error":
            br.close()
            soup.decompose()
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
        # If the game has no reviews
        except ValueError:
            self.positive_reviews = None
            self.negative_reviews = None

        # Get metascore
        try:
            result = soup.find("div", id="game_area_metascore").text
            score = result[:result.find("/")]
            int(score)
            self.metascore = score
        # Games without a metascore are labelled "N/A" on the site
        except (ValueError, AttributeError):
            self.metascore = None

        # Find on which operating systems the game runs
        self.operating_systems = []
        if soup.find("span", {"class": "platform_img win"}):
            self.operating_systems.append("win")
        if soup.find("span", {"class": "platform_img mac"}):
            self.operating_systems.append("mac")
        if soup.find("span", {"class": "platform_img linux"}):
            self.operating_systems.append("linux")

        # Down here so that if the store page doesn't exist, is set to None
        self.store_url = url

        br.close()
        soup.decompose()

    def print_game(self):
        print "appid:", self.app_id
        print "image URL:", self.image_url
        print "name:", self.name
        print "tags:", self.tags
        print "metascore:", self.metascore
        print "positive review count:", self.positive_reviews
        print "negative review count:", self.negative_reviews
        print "features:", self.features
        print "Store URL:", self.store_url
        print "Operating systems:", self.operating_systems

    # Made above list comprehensions easier to reason
    def has_tags(self, tags):
        if type(tags) == str:
            if tags not in self.tags:
                return False
        elif type(tags) == list:
            for i in tags:
                if i not in self.tags:
                    return False
        else:
            return False
        return True
