"""
Functions for interacting with data in the database
"""

import sqlite3
import sys
from xmlrpc.client import Boolean
import bcrypt
from enum import Enum

DATABASE_PATH = "mylib/database.sqlite"


def get_db_connection():
    """Connects to the database

    Returns:
        Connection: the connection to the database
    """
    connection = None
    try:
        connection = sqlite3.connect(DATABASE_PATH)

        # Make it so results are dicts, not tuples
        connection.row_factory = sqlite3.Row

        return connection
    except sqlite3.Error as exception:
        print(f"Error while getting db connection: {exception}")
        if connection is not None:
            connection.close()
        return None


def reset_database():
    """
    Deletes and re-creates all the database tables
    """
    connection = None
    try:
        connection = get_db_connection()

        with open('mylib/schema.sql', encoding="utf-8") as sql_file:
            connection.executescript(sql_file.read())

        connection.commit()

    except sqlite3.Error as exception:
        print(f"Error while setting up database: {exception}")
        if connection is not None:
            connection.close()
    else:
        print("Successfully set up database")


def get_messages():
    """Fetches all the messages from the database

    Returns:
        List: a list of dictionaries with `username` and `content` keys
    """
    try:
        with (connection := get_db_connection()):
            return connection.execute("SELECT * FROM messages ORDER BY created DESC")

    except sqlite3.Error as exception:
        print(f"Error while getting all messages: {exception}")
        sys.exit()


def add_message(username, content):
    """Inserts a message into the database

    Args:
        username (str): the poster's username
        content (str): the message's text content
    """
    try:
        with (connection := get_db_connection()):
            connection.execute(
                "INSERT INTO messages (username, content) VALUES (?,?)",
                (username, content),
            )
            connection.commit()

    except sqlite3.Error as exception:
        print(
            f"Error while adding message with username {username!r} "
            f"and content {content!r}: {exception}"
        )


class FetchAmount(Enum):
    ZERO = 0
    ONE = 1
    ALL = 2


def execute_query(query, args_tuple, fetch_amount, error_msg):
    try:
        with (connection := get_db_connection()):
            result = connection.execute(query, args_tuple)
            connection.commit()
            if fetch_amount == FetchAmount.ONE:
                return result.fetchone()
            if fetch_amount == FetchAmount.ALL:
                return result.fetchall()
            if fetch_amount == FetchAmount.ZERO:
                return None
    except sqlite3.Error as exception:
        print(
            f"[ERROR] {error_msg}\n"
            f"QUERY: {query!r}\n"
            f"ARGS TUPLE: {args_tuple!r}\n"
            f"EXCEPTION: {exception}"
        )
        sys.exit()


def get_user_by_username(username):
    """Returns the user with the given username, or None if it can't be found

    Args:
        username (str): the user's username

    Returns:
        sqlite3.Row: a User dict
    """
    return execute_query(
        "SELECT * FROM users WHERE username = ?",
        (username,),
        FetchAmount.ONE,
        f"Failed to fetch user with username {username}",
    )


def get_user_by_email(email):
    """Returns the user with the given email, or None if it can't be found

    Args:
        email (str): the user's email

    Returns:
        sqlite3.Row: a User dict
    """
    return execute_query(
        "SELECT * FROM users WHERE email = ?",
        (email,),
        FetchAmount.ONE,
        f"Failed to fetch user with email {email}",
    )


def get_user_by_username_or_email(username_or_email):
    """Returns the user with the given username or email, or None if it can't be found

    Args:
        username_or_email (str): the user's username or email

    Returns:
        sqlite3.Row: a User dict
    """
    return execute_query(
        "SELECT * FROM users WHERE username = ? or email = ?",
        (username_or_email,username_or_email),
        FetchAmount.ONE,
        f"Failed to fetch user with username or email {username_or_email}",
    )

def create_user(username, email, password, is_admin = False):
    """Adds a user to the database

    Args:
        username (str): the user's username
        email (str): the user's email
        password (str): the user's password
        is_admin (bool, optional): Whether the user should be an admin. Defaults to False.
    """
    password_hash = bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt())
    is_admin = 1 if is_admin else 0 # bools in sqlite are ints
    execute_query(
        "INSERT INTO users (username, email, password_hash, is_admin) VALUES (?,?,?,?)",
        (username, email, password_hash, is_admin),
        FetchAmount.ZERO,
        "Failed to add new user",
    )



def get_all_users():
    """Fetch all users in the database

    Returns:
        list(sqlite3.Row): a list of User dicts
    """
    return execute_query(
        "SELECT * FROM users", tuple(), FetchAmount.ALL, "Failed to fetch all users"
    )


def check_password(username, password):
    """Checks to see if a username and password combination is correct

    Args:
        username (str): The user's username
        password (str): The user's provided password

    Returns:
        bool: whether the username exists and the password is correct
    """
    user = get_user_by_username(username)
    if user is None:
        return False
    return bcrypt.checkpw(bytes(password,"utf-8"), user["password_hash"])