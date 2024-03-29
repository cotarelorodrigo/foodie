class NotFoundException(Exception):
    def __init__(self, message):
        self.msg = message
        
class InvalidUserInformation(Exception):
    def __init__(self, message):
        self.msg = message

class NotFoundEmail(Exception):
    def __init__(self, message):
        self.msg = message

class AccessDeniedException(Exception):
    def __init__(self, message):
        self.msg = message

class ShopNotFound(Exception):
    def __init__(self, message):
        self.msg = message

class InvalidInformation(Exception):
    def __init__(self, message):
        self.msg = message

class InvalidStateChange(Exception):
    def __init__(self, message):
        self.msg = message

class InvalidQueryParameters(Exception):
    def __init__(self, message):
        self.msg = message

class NotEnoughFavourPoints(Exception):
    def __init__(self, message):
        self.msg = message