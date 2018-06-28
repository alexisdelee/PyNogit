from uuid import uuid4
from .git import Git

class Commit(Git):
    def __init__(self, tree, parentTree = None):
        super().__init__()
        self.__tree = tree
        self.__parentTree = parentTree

    @staticmethod
    def getLatest(branch):
        return Git().shell("git show --pretty=format:\"%H\" --no-patch {0}".format(branch))

    @staticmethod
    def tag(commit, tag, rawTag):
        Git().shell("git tag -a {0} {1} -m {2}".format(tag, commit, rawTag))

    @staticmethod
    def untagged(tag):
        Git().shell("git tag --delete {0}".format(tag))

    @staticmethod
    def getByTag(tag):
        return Git().shell("git rev-list -n 1 {0}".format(tag))

    @staticmethod
    def getAllTags(commit):
        return Git().shell("git tag --contains {0}".format(commit)).split()

    def commit(self):
        if self.__parentTree is None:
            return self.shell("git commit-tree {0}".format(self.__tree), str(uuid4()))
        else:
            return self.shell("git commit-tree {0] -p {1}".format(self.__tree, self.__parentTree), str(uuid4()))
