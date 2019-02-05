import pytest

from pynogit import NoGit

TABLE_NAME = "tests"

def test_insert_simple_type(db):
    db.purge()

    db.set("a", 1, TABLE_NAME)
    assert db.get("a", TABLE_NAME) == 1

    db.mset({ "a": 2, "b": 3 }, TABLE_NAME)
    assert db.get("a", TABLE_NAME) == 2
    assert db.get("b", TABLE_NAME) == 3

def test_insert_complexe_type(db):
    db.purge()

    db.lpush("a", [ 2, 3 ], TABLE_NAME)
    db.lpush("a", [ 1 ], TABLE_NAME)
    assert db.get("a", TABLE_NAME) == [ 1, 2, 3 ]

    db.rpush("a", [ 4, 5 ], TABLE_NAME)
    assert db.get("a", TABLE_NAME) == [ 1, 2, 3, 4, 5 ]

    db.lpush("b", [ "a" ], TABLE_NAME)
    db.rpush("b", [ "b", "c" ], TABLE_NAME)
    assert db.mget([ "a", "b" ], TABLE_NAME) == { "a": [ 1, 2, 3, 4, 5 ], "b": [ "a", "b", "c" ] }

def test_update_with_incr_decr(db):
    db.purge()

    db.set("a", 1, TABLE_NAME)

    db.incrby("a", 2, TABLE_NAME)
    assert db.get("a", TABLE_NAME) == 3

    db.decrby("a", 1, TABLE_NAME)
    assert db.get("a", TABLE_NAME) == 2

    db.incr("a", TABLE_NAME)
    assert db.get("a", TABLE_NAME) == 3

    db.decr("a", TABLE_NAME)
    assert db.get("a", TABLE_NAME) == 2

def test_remove(db):
    db.purge()

    db.set("a", 1, TABLE_NAME)
    
    db.delete("a", TABLE_NAME)
    assert db.get("a", TABLE_NAME) is None
