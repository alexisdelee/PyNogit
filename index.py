# import os, sys, inspect
# currentdir = os .path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0, parentdir)

from pynogit import NoGit

# nogit = NoGit(username="master", credentials="HLGfzDLCuvLqT8VSnLoQ", database="mcdo")
nogit = NoGit(username="master", database="mcdo")

nogit.mset({ "a": 12, "b": 20 }, "ingredients")
print(nogit.get("a", "ingredients"))
nogit.mset({ "a": 13, "b": 20 }, "products")
print(nogit.get("a", "products"))

# view all commits git: log --reflog --oneline --source 4vimquqvtrijmnmigqjpjspnjuttruovorokmurt
# get all tags from a commit: git tag --contains a1ae7cb

transactions = nogit.getAllTransactions(True)
print(transactions)

nogit.savepoint("test")
