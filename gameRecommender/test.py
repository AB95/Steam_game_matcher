import django

from user import User
from gameRecommender import utils, crud
import time
from game import Game


if __name__ == "__main__":
    # tests go here

    django.setup()

    # game = Game("262060", "x", "Hero Siege")
    # print game.operating_systems

    # start = time.time()
    #

    # usr1 = User("76561198032447319")
    # games = usr1.update_games()
    # print [i.operating_systems for i in games.keys() if games[i] > 0 and "linux" in i.operating_systems]

    # start = time.time()
    # usr1 = User("76561198000611224")
    # print time.time() - start
    # usr2 = User("76561198017902347")
    # print time.time() - start
    # usr3 = User("76561197971026489")
    # print time.time() - start
    # games = utils.get_matching_games([usr1, usr2, usr3])
    # games = utils.filter_by_os(games, "linux")
    # games = utils.filter_by_tags(games, ["Co-op", "RPG", "Sandbox"])
    # games = utils.filter_by_features(games, "Co-op")
    # print time.time() - start

    start = time.time()
    bouch = User("alexishbob2")
    games = bouch.games
    games = utils.filter_by_os(games, "linux")
    games = utils.filter_by_tags(games, ["Co-op", "RPG", "Sandbox"])
    games = utils.filter_by_features(games, "Co-op")
    print time.time() - start

    print games

    # usr2 = User("76561197996666573")
    # usr3 = User("76561198047144666")

    # mid = time.time()
    # print mid - start
    #
    # for i in xrange(100):
    #     utils.get_matching_games([usr1, usr2, usr3])
    #
    # print (time.time() - mid)/100

    # print time.time() - start
    #
    # games = utils.get_matching_games([usr1, usr2, usr3])
    # print time.time() - start
    # [i.name for i in utils.filter_by_tags([i for i in utils.filter_by_features(games, "Multi-player")], "Sandbox")]
    # print time.time() - start


    # start = time.time()
    #
    # usr1 = User("76561198000611224").update_games()
    # usr2 = User("76561198017902347").update_games()
    # usr3 = User("76561197971026489").update_games()
    # usr4 = User("76561197981142609").update_games()
    # usr5 = User("76561198026221141").update_games()
    #
    # print time.time() - start
    #
    # games = utils.get_matching_games([usr1, usr2, usr3, usr4, usr5])
    #
    # print len([i.name for i in utils.filter_by_features([i for i in utils.filter_by_tags(games, ["Sandbox", "Adventure"])], "Single-player")])
    #
    # print time.time() - start

    # print time.time() - mid

    # 76561198032447319 Bouch
    # 76561198021143995 Matt
    # 76561198018709098 Dan
    # 76561198189868938 Squacks
    # 76561198189798351 Bizzle

    # people with most games on Steam:
    # 76561198000611224 76561198017902347 76561197971026489 76561197981142609 76561198026221141

    # people with ~2000 games:
    # 76561198039643526 76561197996666573 76561198047144666 76561198030576533 76561198035346209
