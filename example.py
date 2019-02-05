from pynogit import NoGit

nogit = NoGit(username = "master", credentials = "master", database = "mcdo")

nogit.mset({ "a": 12, "b": 20 }, "ingredients")
print(nogit.get("a", "ingredients"))

# nogit.rpush("c", [ 3 ], "ingredients")
# nogit.expire("c", "ingredients", 10)
print(nogit.lrange("c", 0, 1, "ingredients"))

# nogit.savepoint("test")

# nogit.purge()
