"""
Tests for the application (via pytest)
"""
import pytest
from . import db_functions

@pytest.fixture
def _connection():
    """A fixture which returns a connection to the database

    Returns:
        Connection: a connection to the sqlite database
    """
    return db_functions.get_db_connection()

@pytest.fixture
def _with_added_users():
    """
    A fixture which resets the database and populates it with some users
    """
    db_functions.reset_database()
    db_functions.create_user("Alice", "alice@site.com", "alice_pass")
    db_functions.create_user("Bob", "bob@site.com", "bob_pass")
    db_functions.create_user("Charles", "charles@site.com", "charles_pass")



def test_get_db_connection(_connection):
    """Ensures we can get a connection to the database
    """
    assert _connection is not None


def test_get_users(_with_added_users):
    """Tests the get_all_users() function

    Args:
        with_added_users (Fixture): a fixture that pre-populates the database with users
    """
    assert len(db_functions.get_all_users()) == 4 # 3 from fixture plus one admin user


def test_check_password(_with_added_users):
    """Tests the check_password() function

    Args:
        with_added_users (Fixture): a fixture that pre-populates the database with users
    """
    assert db_functions.check_password("Alice", "alice_pass")
    assert not db_functions.check_password("Bob", "wrong_pass")
    assert not db_functions.check_password("nonexistent_user", "alice_pass")

def test_get_user(_with_added_users):
    """Checks the functions that retrieve users

    Args:
        with_added_users (Fixture): a fixture that pre-populates the database with users
    """
    assert db_functions.get_user_by_username("Bob")["email"] == "bob@site.com"
    assert db_functions.get_user_by_email("alice@site.com")["username"] == "Alice"
    assert db_functions.get_user_by_username_or_email("Charles")["email"] == "charles@site.com"
    assert db_functions.get_user_by_username_or_email("charles@site.com")["username"] == "Charles"

def test_get_nonexistent_user(_with_added_users):
    """Checks the functions that retrieve users with bogus input

    Args:
        with_added_users (Fixture): a fixture that pre-populates the database with users
    """
    assert db_functions.get_user_by_username("nonexistent_user") is None
    assert db_functions.get_user_by_email("nonexistent_user") is None
    assert db_functions.get_user_by_username_or_email("nonexistent_user") is None


def test_add_posts(_with_added_users):
    """Tests the ability to add posts"""
    db_functions.create_post("My post","Hello, world!", 2)