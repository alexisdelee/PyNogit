import pytest

from pynogit import NoGit

@pytest.fixture
def db():
    return NoGit(username = "4NERU7V7ua", credentials = "KumW6nPPRA", database = "p2ouvFBbx6")
