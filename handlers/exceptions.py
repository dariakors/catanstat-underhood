class InvalidTurnStatusException(BaseException):
    pass


class CommonApplicationException(Exception):
    status_code = None

    def __init__(self, message):
        self.message = message

    def to_dict(self):
        return {"error": self.message}


class BadRequest(CommonApplicationException):
    status_code = 400
