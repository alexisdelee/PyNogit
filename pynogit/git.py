from subprocess import run, PIPE
from os import getcwd, environ

class Git:
    def __init__(self):
        pass

    @staticmethod
    def isWorkspace():
        try:
            response = Git().shell("git rev-parse --is-inside-work-tree")
            return True if response is "true" else False
        except Exception:
            return False

    @staticmethod
    def setWorkspace():
        Git().shell("git init")

    def shell(self, command, stdin = None):
        if environ.get("PYNOGIT_DB") is None:
            raise Exception("PYNOGIT_DB is undefined")

        response = None
        if stdin is None:
            response = run(command, stdout = PIPE, stderr = PIPE, shell = True, cwd = environ.get("PYNOGIT_DB"))
        else:
            response = run(command, stdout = PIPE, stderr = PIPE, input = stdin.encode("utf-8"), shell = True, cwd = environ.get("PYNOGIT_DB"))

        if response.returncode is not 0:
            if type(response.stderr) is bytes:
                raise Exception(response.stderr.decode("utf-8").strip())
        return response.stdout.decode("utf-8").strip()
