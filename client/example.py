# import os, sys, inspect
# currentdir = os .path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0, parentdir)

from pynogit import NoGit

# nogit = NoGit(username="master", credentials="HLGfzDLCuvLqT8VSnLoQ", database="mcdo")
nogit = NoGit(username="master", database="mcdo")

nogit.mset({ "a": 12, "b": 20 }, "ingredients")
print(nogit.get("a", "ingredients"))

# nogit.rpush("c", [ 3 ], "ingredients")
nogit.expire("c", "ingredients", 10000)
print(nogit.get("c", "ingredients"))

# nogit.savepoint("test")
