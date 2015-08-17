import django

from user import User

if __name__ == "__main__":
    # tests go here
    django.setup()
    user = User(76561198032447319)
    games_list = user.get_games()

    for i in games_list.keys():
        print i.name, games_list[i]
        i.print_game()
        print "===================================="

    # 76561198032447319 Bouch
    # 76561198021143995 Matt
    # 76561198018709098 Dan
    # 76561198189868938 Squacks

    # people with most games on Steam:
    # 76561198000611224 76561198017902347 76561197971026489 76561197981142609 76561198026221141