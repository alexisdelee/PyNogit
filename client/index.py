from flask import Flask, render_template, redirect, request
from flask_cors import CORS
from pynogit import NoGit
from pynogit.helper import Helper

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app)

authentication = {
    "username": None,
    "password": None,
    "database": None,
    "collection": None,
    "instance": None
}

# GET

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html", data = {
        "username": "" if authentication["username"] is None else authentication["username"],
        "password": "" if authentication["password"] is None else authentication["password"],
        "database": "" if authentication["database"] is None else authentication["database"]
    })

@app.route("/collections/<collection>", methods=["GET"])
def collection(collection):
    blobs = authentication["instance"].__get_collection__(collection)
    return render_template("collection.html", data = {
        "collection": collection,
        "blobs": blobs
    })

# POST
@app.route("/sign", methods=["POST"])
def sign():
    try:
        body = Helper.JSONDecoding(request.data)
        print(body)
        assert type(body.get("username")) is str
        assert type(body.get("password")) is str or body.get("password") is None
        assert type(body.get("database")) is str
        assert type(body.get("collection")) is str

        authentication["username"] = body.get("username")
        authentication["password"] = body.get("password")
        authentication["database"] = body.get("database")

        if body.get("password") is None:
            authentication["instance"] = NoGit(username=body.get("username"), database=body.get("database"))
        else:
            authentication["instance"] = NoGit(username=body.get("username"), credentials=body.get("password"), database=body.get("database"))

        return Helper.JSONEncoding({ "status": True })
    except AssertionError:
        return Helper.JSONEncoding({ "error": "bad type" })
    except Exception as e:
        print(e)
        return Helper.JSONEncoding({ "error": str(e) })

# PUT

@app.route("/blobs", methods=["PUT"])
def add_blob():
    try:
        body = Helper.JSONDecoding(request.data)
        assert type(body.get("key")) is str
        assert type(body.get("value")) in [ int, float, str, list ]
        assert type(body.get("collection")) is str

        if type(body.get("value")) is list:
            authentication["instance"].delete(body.get("key"), body.get("collection"))
            authentication["instance"].lpush(body.get("key"), body.get("value"), body.get("collection"))
        else:
            authentication["instance"].set(body.get("key"), body.get("value"), body.get("collection"))
        return Helper.JSONEncoding({ })
    except AssertionError:
        return Helper.JSONEncoding({ "error": "bad type" })
    except Exception as e:
        return Helper.JSONEncoding({ "error": str(e) })

@app.route("/blobs/expire", methods=["PUT"])
def expire_blob():
    try:
        body = Helper.JSONDecoding(request.data)
        assert type(body.get("key")) is str
        assert type(body.get("collection")) is str
        assert type(body.get("seconds")) is int

        response = authentication["instance"].__expire__(body.get("key"), body.get("collection"), body.get("seconds"))
        return Helper.JSONEncoding({ "status": response })
    except AssertionError:
        return Helper.JSONEncoding({ "error": "bad type" })
    except Exception as e:
        return Helper.JSONEncoding({ "error": str(e) })

# DELETE

@app.route("/blobs", methods=["DELETE"])
def delete_blob():
    try:
        body = Helper.JSONDecoding(request.data)
        assert type(body.get("key")) is str
        assert type(body.get("collection")) is str

        response = authentication["instance"].delete(body.get("key"), body.get("collection"))
        return Helper.JSONEncoding({"status": response})
    except AssertionError:
        return Helper.JSONEncoding({ "error": "bad type" })
    except Exception as e:
        return Helper.JSONEncoding({ "error": str(e) })

# @app.route("/commits")
# def commits():
#     nogit = NoGit(username="master", database="mcdo")
#     return render_template("history.html", data={ "commits": nogit.getAllTransactions(True) })
#
# @app.route("/commits/<commit>")
# def commit(commit):
#     nogit = NoGit(username="master", database="mcdo")
#     collections = nogit.getAllCollections(commit)
#     print(collections)
#     print(nogit.__get_collection__("05ef19cb72f6894100968e1de8336ec6e6c6be3c"))
#     print(list(map(lambda c: nogit.__get_collection__(c), collections)))
#     return render_template("content.html", data = {
#         # collections: list(map(lambda c: c + "a", collections))
#     })

if __name__ == "__main__":
    app.run()
