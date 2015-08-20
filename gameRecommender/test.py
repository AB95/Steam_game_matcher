import django

from user import User
from gameRecommender import utils
import time


if __name__ == "__main__":
    # tests go here

    django.setup()

    start = time.time()
    #
    usr1 = User("76561198039643526")
    # usr2 = User("76561198032447319")
    # usr3 = User("76561198021143995")
    #
    mid = time.time()
    print mid - start
    #
    # for i in xrange(100):
    #     utils.get_matching_games(usr1, usr2, usr3)
    #
    # print (time.time() - mid)/100
    #
    # print len([i.name for i in utils.get_matching_games(usr1, usr2, usr3)])

    # print User("76561198189798351").games
    #
    # start = time.time()
    #
    # usr1 = User("76561198000611224")
    # usr2 = User("76561198017902347")
    # usr3 = User("76561197971026489")
    # usr4 = User("76561197981142609")
    # usr5 = User("76561198026221141")
    #
    # mid = time.time()
    # print "Users processed:", mid - start
    #
    # for i in xrange(100):
    #     utils.get_matching_games(usr1, usr2, usr3, usr4, usr5)
    #
    # final = (time.time() - mid) / 100
    #
    # print final

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
