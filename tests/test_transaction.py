import pytest

from string import ascii_uppercase, ascii_lowercase, digits
from random import choices
from pynogit import NoGit

TABLE_NAME = "tests"

def test_transaction(db):
    db.purge()

    random_tag_name = "".join(choices(ascii_uppercase + ascii_lowercase + digits, k = 10))

    db.set("a", 1, TABLE_NAME)
    assert db.get("a", TABLE_NAME) == 1

    transaction = db.savepoint(random_tag_name)
    assert db.get("a", TABLE_NAME) == 1

    db.rollback(random_tag_name)
    db.set("a", 2, TABLE_NAME)
    assert db.get("a", TABLE_NAME) == 2

    transaction.rollback()
    assert db.get("a", TABLE_NAME) == 1

    db.release(random_tag_name)

def test_transaction_with_begin(db):
    db.purge()

    db.set("a", 1, TABLE_NAME)
    assert db.get("a", TABLE_NAME) == 1

    transaction = db.begin()
    db.set("a", 2, TABLE_NAME)

    transaction.rollback()
    assert db.get("a", TABLE_NAME) == 1
