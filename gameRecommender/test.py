import django

import utils
from user import User


if __name__ == "__main__":
    # tests go here
    # django.setup()
    # user = User(76561198032447319)
    # games_list = user.get_games()
    #
    # for i in games_list.keys():
    #     print i.name, games_list[i]
    #     i.print_game()
    #     print "===================================="

    django.setup()
    import time
    start = time.time()
    print [i.name for i in utils.get_matching_games([User(76561198032447319), User(76561198018709098), User(76561198189868938)])]
    print time.time() - start

    # 76561198032447319 Bouch
    # 76561198021143995 Matt
    # 76561198018709098 Dan
    # 76561198189868938 Squacks
    # 76561198189798351 Bizzle

    # people with most games on Steam:
    # 76561198000611224 76561198017902347 76561197971026489 76561197981142609 76561198026221141
