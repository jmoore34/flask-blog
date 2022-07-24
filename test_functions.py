"""
Tests for the application (via pytest)
"""
from app import get_db_connection,get_messages,add_message



def test_get_db_connection():
    """Ensures we can get a connection to the database
    """
    assert get_db_connection() is not None


def messages_are_valid():
    """
    Ensures messages from get_messages()
     follow the right format
    """
    for message in get_messages():
        assert isinstance(message.content, str)
        assert isinstance(message.username, str)

def can_insert_message():
    """
    Inserts a message and ensures it was inserted
    """
    add_message("bob", "hello")
    assert get_messages()[-1]["username"] == "bob"
    assert get_messages()[-1]["content"] == "hello"
