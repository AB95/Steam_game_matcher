

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