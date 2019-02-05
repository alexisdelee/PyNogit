import pytest

from pynogit import NoGit

@pytest.fixture
def db():
    return NoGit(username = "master", credentials = "master", database = "mcdo")
