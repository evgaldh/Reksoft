class HTTPError(Exception):
    def __init__(self, status, message=None):
        self.status = status
        if not isinstance(message, list):
            message = [message]
        self.message = message