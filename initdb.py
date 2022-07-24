"""
Initializes the database by running schema.sql
"""

import sqlite3

print("Setting up database...")

CONNECTION = None
try:
    connection = sqlite3.connect('database.db')

    with open('schema.sql', encoding="utf-8") as f:
        connection.executescript(f.read())

    connection.commit()

except sqlite3.Error as exception:
    print(f"Error while setting up database: {exception}")
    if connection is not None:
        connection.close()
else:
    print("Successfully set up database")
