from subprocess import run, PIPE
from os import getcwd

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
        response = None
        if stdin is None:
            response = run(command, stdout = PIPE, stderr = PIPE, cwd = getcwd())
        else:
            response = run(command, stdout = PIPE, stderr = PIPE, input = stdin.encode("utf-8"), cwd = getcwd())

        if response.returncode is not 0:
            if type(response.stderr) is bytes:
                raise Exception(response.stderr.decode("utf-8").strip())
        return response.stdout.decode("utf-8").strip()
