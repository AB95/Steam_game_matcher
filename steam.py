import urllib2 as urllib
import json
import xml.etree.ElementTree as ET
import BeautifulSoup as BS
from selenium import webdriver


def _getOwnedGamesByUserID(userID, includeFree):
    url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=E770C55138B535447F8678136EFC9285&steamid=" + \
          userID + "&format=json&include_played_free_games=" + str(includeFree) + "&include_appinfo=1"
    response = urllib.urlopen(url)
    data = json.loads(response.read())

    games = []

    for i in data["response"]["games"]:
        games.append((i["name"], i["appid"]))

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
            games = [x for x in games if x in gamesList]

        return games

    elif len(users) == 1:
        return getOwnedGames(users[0])


def getTags(game):
    url = "http://store.steampowered.com/app/" + str(game[1])

    driver = webdriver.Firefox()
    driver.get(url)
    if "agecheck" in driver.current_url:
        driver.find_element_by_xpath("//select[@name='ageYear']/option[text()='1990']").click()
        driver.find_element_by_class_name("btnv6_blue_hoverfade").click()
    html = driver.page_source
    driver.close()

    soup = BS.BeautifulSoup(html)
    scriptResults = soup('script',{'type' : 'text/javascript'})
    tag = scriptResults[26]
    tagString = tag.string
    tags = tagString[tagString.index("["):tagString.index(",", tagString.index("]"))]

    data = json.loads(tags)
    return [x["name"] for x in data]


def getMetaScore(game):
    url = "http://store.steampowered.com/app/" + str(game[1])

    driver = webdriver.Firefox()
    driver.get(url)
    if "agecheck" in driver.current_url:
        driver.find_element_by_xpath("//select[@name='ageYear']/option[text()='1990']").click()
        driver.find_element_by_class_name("btnv6_blue_hoverfade").click()
    html = driver.page_source
    driver.close()

    soup = BS.BeautifulSoup(html)
    result = soup.find("div", id="game_area_metascore").text
    return result[:result.find("/")]

