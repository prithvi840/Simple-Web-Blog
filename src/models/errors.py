
class UserError(Exception):
    def __int__(self, message):
        self.message = message

class UserNotExistsError(UserError):
    def __init__(self, message):
        self.message = message

class IncorrectPasswordError(UserError):
    def __init__(self, message):
        self.message = message

class UserAlreadyRegisteredError(UserError):
    def __init__(self, message):
        self.message = message

class InvalidEmailError(UserError):
    def __init__(self, message):
        self.message = message

