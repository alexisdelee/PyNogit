from .git import Git

class Document(Git):
    def __init__(self, data):
        super().__init__()
        self.__data = data

    def indexing(self):
        return self.shell("git hash-object -w --stdin", self.__data)
