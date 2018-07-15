from time import time
from os import urandom
from .helper import Helper
from .git import Git
from .branch import Branch
from .commit import Commit
from .collection import Collection
from .document import Document
from .transaction import Transaction

class Structure:
    integer = 1
    float   = 2
    string  = 4
    list    = 8

    def __init__(self, value, expire, structure):
        self.value = value
        self.expire = -1 if expire is None else expire
        self.structure = structure

    def abstraction(self):
        t = time()

        return {
            "value": self.value,
            "__datatype__": Structure.getDatatype(self.value),
            "__expire__": self.expire,
            "__created_at__": t if self.structure is None else self.structure["__created_at__"],
            "__updated_at__": t
        }

    @staticmethod
    def getDatatype(value):
        t = type(value)
        if t is float:
            return Structure.float
        elif t is int:
            return Structure.integer
        elif t is str:
            return Structure.string
        elif t is list:
            return Structure.list

class NoGit:
    def __init__(self, database, username, credentials = None):
        assert type(database) is str
        assert type(username) is str
        assert type(credentials) is str or credentials is None

        self.__database = Helper.hash(database)
        self.__username = Helper.hash(username)
        self.__rawCredentials = credentials
        self.__credentials = None if credentials is None else Helper.hash(credentials)
        self.__aes = None

        if Git.isWorkspace() is False:
            Git.setWorkspace()

        if Branch.have(Helper.readable(self.__username)) is False:
            self.__init_user__()
        else:
            data = self.__get_collection__("__credentials__")
            if data.get("username", None) == self.__username and data.get("password", None) == self.__credentials:
                self.__aes = data.get("aes", None)
                if self.__aes is not None:
                    key = Helper.Cipher.simpleDecryption(self.__aes.rjust(64), credentials.rjust(64))
                    self.__aes = Helper.hexToBytes(key)
                return

            raise Exception("bad credentials")

    def __init_user__(self):
        self.__aes = None if self.__credentials is None else urandom(32)
        self.__save__({
            "username": self.__username,
            "password": self.__credentials,
            "aes": None if self.__aes is None else Helper.Cipher.simpleEncyption(Helper.bytesToHex(self.__aes).rjust(64), self.__rawCredentials.rjust(64))
        }, "__credentials__")
        self.savepoint(Commit.uuid())

    def __set_collection__(self, data, collection):
        assert type(data) is str
        assert type(collection) is str

        data = data if collection == "__credentials__" or self.__aes is None else Helper.Cipher.advancedEncryption(data, self.__aes)
        blob = Document(data).indexing()
        return {
            "blob": blob,
            "tree": Collection(blob).store(self.__database, Helper.readable(Helper.hash(collection)))
        }

    def __get_collection__(self, collection):
        assert type(collection) is str

        try:
            data = Collection.restore(Helper.readable(self.__username), self.__database, Helper.readable(Helper.hash(collection)))
            data = data if collection == "__credentials__" or self.__aes is None else Helper.Cipher.advancedDecryption(data, self.__aes)

            return Helper.JSONDecoding(data)
        except Exception as e:
            return {}

    def __check_expire__(self, key, collection, data):
        assert type(key) is str
        assert type(collection) is str
        assert type(data) is dict or data is None

        data = self.__get_collection__(collection) if data is None else data
        t = time()

        if self.exists(key, collection, data):
            if data[key]["__expire__"] is not -1 and (t - data[key]["__updated_at__"] > data[key]["__expire__"]):
                return True
        return False

    def __expire__(self, key, collection, seconds):
        assert type(key) is str
        assert type(collection) is str
        assert type(seconds) is int

        data = self.__get_collection__(collection)
        if self.exists(key, collection, data):
            data[key] = Structure(data[key]["value"], seconds, data[key]).abstraction()
            self.__save__(data, collection)
            return True
        return False

    def __delete__(self, key, collection, data = None):
        assert type(key) is str
        assert type(collection) is str
        assert type(data) is dict or data is None

        data = self.__get_collection__(collection) if data is None else data
        if self.exists(key, collection, data):
            del data[key]
            self.__save__(data, collection)
            return True
        else:
            return False

    def __save__(self, data, collection):
        assert type(data) is dict
        assert type(collection) is str

        blob, tree = self.__set_collection__(Helper.JSONEncoding(data), collection).values()
        commit = Commit(tree).commit()
        Branch(commit).attach(Helper.readable(self.__username))

    def __push__(self, key, values, isLeft, collection):
        assert type(key) is str
        assert type(values) is list
        assert type(isLeft) is bool
        assert type(collection) is str

        for i in range(0, len(values)):
            assert type(values[i]) in [ int, float, str ]

        data = self.__get_collection__(collection)
        if self.exists(key, collection, data) and data[key]["__datatype__"] & Structure.list:
            arr = values + data[key]["value"] if isLeft else data[key]["value"] + values
            data[key] = Structure(arr, None, data[key]).abstraction()
        else:
            data[key] = Structure(values, None, None).abstraction()
        self.__save__(data, collection)
        return len(values)

    def __pop__(self, key, isLeft, collection):
        assert type(key) is str
        assert type(isLeft) is bool
        assert type(collection) is str

        data = self.__get_collection__(collection)
        if self.exists(key, collection, data):
            if data[key]["__datatype__"] & Structure.list:
                if len(data[key]["value"]) is 0:
                    return None

                item = data[key]["value"][0] if isLeft else data[key]["value"][-1]
                arr = data[key]["value"][1:] if isLeft else data[key]["value"][:-1]

                data[key] = Structure(arr, None, data[key]).abstraction()
                self.__save__(data, collection)

                return item
        raise Exception("bad type: expected list")

    def exists(self, key, collection, data = None):
        assert type(key) is str
        assert type(collection) is str
        assert type(data) is dict or data is None

        data = self.__get_collection__(collection) if data is None else data
        # try:
        #     data[key]
        #     return True
        # except LookupError:
        #     return False
        return data.get(key)

    def mset(self, items, collection, expire = None):
        assert type(items) is dict
        assert type(collection) is str
        assert type(expire) is int or expire is None

        data = self.__get_collection__(collection)
        bk = dict(data)
        for key, value in items.items():
            assert type(value) in [ int, float, str ]

            if self.exists(key, collection, data):
                if expire is None and data[key] is not None and value == data[key]["value"]:
                    continue
                data[key] = Structure(value, expire, data[key]).abstraction()
            else:
                data[key] = Structure(value, expire, None).abstraction()

        if data != bk:
            self.__save__(data, collection)

    def set(self, key, value, collection, expire = None):
        self.mset({ key: value }, collection, expire)

    def mget(self, keys, collection):
        assert type(keys) is list
        assert type(collection) is str

        data = self.__get_collection__(collection)
        response = {}

        for i in range(0, len(keys)):
            if self.exists(keys[i], collection, data):
                if self.__check_expire__(keys[i], collection, data):
                    self.__delete__(keys[i], collection, data)
                    response[keys[i]] = None
                else:
                    response[keys[i]] = data[keys[i]]["value"]
            else:
                response[keys[i]] = None
        return response

    def get(self, key, collection):
        return self.mget([ key ], collection)[ key ]

    def lrange(self, key, a, b, collection):
        assert type(key) is str
        assert type(a) is int
        assert type(b) is int
        assert type(collection) is str

        data = self.__get_collection__(collection)
        if self.exists(key, collection, data) is None:
            return None
        else:
            if self.__check_expire__(key, collection, data):
                self.__delete__(key, collection, data)
                return None

            for i in range(a, b - a):
                if data[key]["__datatype__"] & Structure.list:
                    return data[key]["value"][a:b]
                else:
                    raise Exception("bad type: expected list")

        # if self.exists(key, collection, data):
        #     if data[key]["__datatype__"] & Structure.list:
        #         return data[key]["value"][a:b]
        #     else:
        #         raise Exception("bad type: expected list")
        # return None

    def incrby(self, key, step, collection):
        assert type(key) is str
        assert type(step) is int
        assert type(collection) is str

        data = self.__get_collection__(collection)
        try:
            if data[key] is not None:
                if data[key]["__datatype__"] & ( Structure.integer | Structure.float ):
                    data[key] = Structure(data[key]["value"] + step, None, data[key]).abstraction()
                    self.__save__(data, collection)
                else:
                    raise Exception("bad type: expected number")
        except LookupError:
            raise Exception("unknown key")

    def incr(self, key, collection):
        self.incrby(key, 1, collection)

    def descr(self, key, collection):
        self.incrby(key, -1, collection)

    def decrby(self, key, step, collection):
        self.incrby(key, step * -1, collection)

    def delete(self, key, collection):
        assert type(key) is str
        assert type(collection) is str

        data = self.__get_collection__(collection)
        return self.__delete__(key, collection, data)

    def ttl(self, key, collection):
        assert type(key) is str
        assert type(collection) is str

        t = time()
        data = self.__get_collection__(collection)

        if self.exists(key, collection, data):
            delta = int(data[key]["__updated_at__"] + data[key]["__expire__"] - t)
            return -1 if delta < 0 else delta
        return -1

    def expire(self, key, collection, seconds):
        assert type(seconds) is int

        if seconds > -1:
            return self.__expire__(key, collection, seconds)
        return False

    def persistent(self, key, collection):
        self.__expire__(key, collection, -1)

    def type(self, key, collection):
        assert type(key) is str
        assert type(collection) is str

        data = self.__get_collection__(collection)
        if self.exists(key, collection, data):
            datatype = data[key]["__datatype__"]
            if datatype & Structure.integer:
                return "integer"
            elif datatype & Structure.float:
                return "decimal"
            elif datatype & Structure.string:
                return "string"
            elif datatype & Structure.list:
                return "list"
        return "none"

    def lpush(self, key, values, collection):
        return self.__push__(key, values, True, collection)

    def rpush(self, key, values, collection):
        return self.__push__(key, values, False, collection)

    def lpop(self, key, collection):
        return self.__pop__(key, True, collection)

    def rpop(self, key, collection):
        return self.__pop__(key, False, collection)

    def begin(self):
        return Transaction(None, None, Helper.readable(self.__username))

    def savepoint(self, tag):
        return Transaction(None, None, Helper.readable(self.__username)).savepoint(tag)

    def rollback(self, tag):
        Transaction(None, None, Helper.readable(self.__username)).rollback(tag)

    def release(self, tag):
        Transaction(None, None, Helper.readable(self.__username)).release(tag)

    def getAllTransactions(self, withTags = False):
        assert type(withTags) is bool

        commits = Branch.getAllCommits(Helper.readable(self.__username))
        for i in range(0, len(commits)):
            commits[i] = {
                "ref": commits[i],
                "tags": list(map(lambda reftag: Commit.readTag(reftag), Commit.getAllTags(commits[i]))) if withTags else []
            }

        return commits

    def getAllCollections(self, commit):
        assert type(commit) is str

        return Commit.getAllCollections(commit)
