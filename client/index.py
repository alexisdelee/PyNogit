from flask import Flask, render_template, redirect, request
from flask_cors import CORS
from pynogit import NoGit
from pynogit.helper import Helper

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app)

# GET

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/collections/<collection>", methods=["GET"])
def collection(collection):
    nogit = NoGit(username="master", database="mcdo")
    blobs = nogit.__get_collection__(collection)
    return render_template("collection.html", data=blobs)

# PUT

@app.route("/blobs", methods=["PUT"])
def add_blob():
    try:
        body = Helper.JSONDecoding(request.data)
        assert type(body.get("key")) is str
        assert type(body.get("value")) in [ int, float, str, list ]
        assert type(body.get("collection")) is str

        nogit = NoGit(username="master", database="mcdo")
        if type(body.get("value")) is list:
            nogit.delete(body.get("key"), body.get("collection"))
            nogit.lpush(body.get("key"), body.get("value"), body.get("collection"))
        else:
            nogit.set(body.get("key"), body.get("value"), body.get("collection"))
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

        nogit = NoGit(username="master", database="mcdo")
        response = nogit.__expire__(body.get("key"), body.get("collection"), body.get("seconds"))
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

        nogit = NoGit(username="master", database="mcdo")
        response = nogit.delete(body.get("key"), body.get("collection"))
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
