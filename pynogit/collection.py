from .git import Git
from .commit import Commit
from .helper import Helper

class Collection(Git):
    def __init__(self, blob):
        super().__init__()
        self.__blob = blob

    @staticmethod
    def restore(branch, database, collection):
        return Git().shell("git show {0}:{1}/{2}".format(branch, database, collection))

    def store(self, database, collection):
        self.shell("git update-index --add --cacheinfo 100644 {0} {1}/{2}".format(self.__blob, database, collection))
        return self.shell("git write-tree")
        # Commit.tag(commit, Helper.readable(Helper.hash(collection)), collection)
