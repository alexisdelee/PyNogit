import pytest

from pynogit import NoGit

TABLE_NAME = "tests"

def test_purge(db):
    db.purge()

    db.set("a", 1, TABLE_NAME)
    db.purge()
    assert db.get("a", TABLE_NAME) is None

def test_exist(db):
    db.purge()

    db.set("a", 1, TABLE_NAME)
    assert db.exists("a", TABLE_NAME) is not None

    db.delete("a", TABLE_NAME)
    assert db.exists("a", TABLE_NAME) is None
