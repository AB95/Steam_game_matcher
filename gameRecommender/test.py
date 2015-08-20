import django

import utils

from user import User


if __name__ == "__main__":
    # tests go here

    django.setup()

    import time

    start = time.time()

    usr1 = User("76561198039643526")
    usr2 = User("76561197996666573")

    mid = time.time()
    print mid - start

    for i in xrange(100):
        utils.get_matching_games(usr1, usr2)

    print (time.time() - mid) / 100

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
