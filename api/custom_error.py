class BadColumnException(Exception):
    def __init__(self, message):
        self.message = "BadColumnException: "+str(message)
        super().__init__(self.message)

class UndefinedErrorException(Exception):
    def __init__(self, message):
        self.message = "UndefinedErrorException: "+str(message)
        super().__init__(self.message)

class FileNotFoundException(Exception):
    def __init__(self, message):
        self.message = "FileNotFoundException: "+str(message)
        super().__init__(self.message)