# import os, sys, inspect
# currentdir = os .path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0, parentdir)

from pynogit import NoGit

# nogit = NoGit(username="master", credentials="HLGfzDLCuvLqT8VSnLoQ", database="mcdo")
nogit = NoGit(username="master", database="mcdo")

nogit.mset({ "a": 10, "b": 20 }, "ingredients")
print(nogit.get("a", "ingredients"))
print(nogit.get("b", "ingredients"))
print(nogit.mget([ "a", "c" ], "ingredients"))
