from .git import Git

class Branch(Git):
    def __init__(self, commit):
        super().__init__()
        self.__commit = commit

    @staticmethod
    def have(branch):
        try:
            Git().shell("git rev-parse --verify --quiet {0}".format(branch))
            return True
        except Exception:
            return False

    @staticmethod
    def getAllCommits(branch):
        return Git().shell("git log --reflog --oneline --source {0} --pretty=%H".format(branch)).split()
    
    @staticmethod
    def purge(branch):
        Git().shell("git branch -D {0}".format(branch))

    def attach(self, branch):
        self.shell("git update-ref refs/heads/{0} {1}".format(branch, self.__commit))
