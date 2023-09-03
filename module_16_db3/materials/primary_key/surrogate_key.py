import sqlite3

ENABLE_FOREIGN_KEY = "PRAGMA foreign_keys = ON;"

CREATE_USER_TABLE = """
DROP TABLE IF EXISTS 'user';
CREATE TABLE 'user' (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(255) NOT NULL,
    email TEXT VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL
) 
"""

CREATE_POST_TABLE = """
DROP TABLE IF EXISTS 'post';
CREATE TABLE 'post' (
    post_id INTEGER PRIMARY KEY AUTOINCREMENT,
    author VARCHAR(255) NOT NULL,
    content TEXT NOT NULL DEFAULT ''
);
"""

CREATE_TABLE_LIKE = """
DROP TABLE IF EXISTS 'like';
CREATE TABLE 'like' (
    like_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES user (user_id) ON DELETE CASCADE,
    post_id INTEGER NOT NULL,
    FOREIGN KEY(post_id) REFERENCES post(post_id) ON DELETE CASCADE 
)
"""


def create_tables() -> None:
    with sqlite3.connect("surrogate.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.executescript(ENABLE_FOREIGN_KEY)
        cursor.executescript(CREATE_USER_TABLE)
        cursor.executescript(CREATE_POST_TABLE)
        cursor.executescript(CREATE_TABLE_LIKE)


if __name__ == '__main__':
    create_tables()
