

class AlreadyInDatabaseException(Exception):
    def __init__(self, value):
        self.value = str(value.app_id) + " " + value.name

    def __str__(self):
        return repr(self.value)


class NotInDatabaseException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ProfileNotFoundException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class PageNotLoadedException(Exception):
    def __init__(self, game_id):
        self.id = game_id

    def __str__(self):
        return repr("Game ID: " + str(self.id))
