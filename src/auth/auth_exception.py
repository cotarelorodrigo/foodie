
class InvalidUserInformation(Exception):
    def __init__(self, message):
        self.msg = message

class NotFoundEmail(Exception):
    def __init__(self, message):
        self.msg = message