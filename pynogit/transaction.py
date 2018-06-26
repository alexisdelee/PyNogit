from .helper import Helper
from .git import Git
from .branch import Branch
from .commit import Commit

class Transaction(Git):
    def __init__(self, commit, tag, username):
        super().__init__()
        self.__commit = Commit.getLatest(username) if commit is None else commit
        self.__tag = tag
        self.__username = username

    def savepoint(self, tag):
        assert type(tag) is str

        tag = Helper.readable(Helper.hash(tag))
        commit = Commit.getLatest(self.__username)

        Commit.tag(commit, tag)
        return Transaction(commit, tag, self.__username)

    def rollback(self, tag = None):
        assert type(tag) is str or tag is None

        if tag is None:
            Branch(self.__commit).attach(self.__username)
        else:
            tag = Helper.readable(Helper.hash(tag))
            commit = Commit.getByTag(tag)

            Branch(commit).attach(self.__username)

    def release(self, tag):
        assert type(tag) is str

        tag = Helper.readable(Helper.hash(tag))
        Commit.untagged(tag)
