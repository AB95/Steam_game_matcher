import BeautifulSoup as bs
import json

import mechanize

import crud
import errors


class Game:

    def __init__(self, appid, image_url, name):
        # Initialise known values
        self.appid = int(appid)
        self.image_url = \
            "http://media.steampowered.com/steamcommunity/public/images/apps/" + str(appid) + \
            "/" + image_url + ".jpg"
        self.name = name

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
            self._scrape_details()
            crud.add_game_db(self)
        else:
            game_info = crud.get_game_info(self.appid)
            self.tags = [i["tags"] for i in game_info.gameTags.filter().values("tags")]
            self.metascore = game_info.metascore
            self.positive_reviews = game_info.positive_review_numbers
            self.negative_reviews = game_info.negative_review_numbers
            self.features = [i["features"] for i in game_info.gameFeatures.filter().values("features")]
            self.store_url = game_info.store_page

    # Scrapes info from the game's site
    def _scrape_details(self):
        url = "http://store.steampowered.com/app/" + str(self.appid)

        # Use driver to generate full HTML
        br = mechanize.Browser()
        response = br.open(url)

        # Make sure 503 code not received. Checking the code can throw an error sometimes, but not with a 503,
        # and so can be effectively silenced
        if response.code == 503:
            self._scrape_details()

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
        print "tags:", self.tags
        print "metascore:", self.metascore
        print "positive review count:", self.positive_reviews
        print "negative review count:", self.negative_reviews
        print "features:", self.features
        print "Store URL:", self.store_url

    # Made above list comprehensions easier to reason
    def has_tags(self, tags):
        for i in tags:
            if i not in self.tags:
                return False
        return True