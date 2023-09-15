import sqlite3
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

BOOKS_DATA = [
    {'id': 0, 'title': 'A Byte of Python', 'author_id': 0},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author_id': 1},
    {'id': 3, 'title': 'War and Peace', 'author_id': 3}
]
AUTHORS_DATA = [
    {'author_id': 0, 'first_name': 'CH', 'last_name': 'Swaroop'},
    {'author_id': 1, 'first_name': 'Herman', 'last_name': 'Melville'},
    {'author_id': 3, 'first_name': 'Leo', 'last_name': 'Tolstoy'}
]

DATABASE_NAME = 'table_books.db'
BOOKS_TABLE_NAME = 'books'
AUTHORS_TABLE_NAME = 'authors'


@dataclass
class Book:
    title: str
    author_id: int
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


@dataclass
class Author:
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    id: Optional[int] = None
    title: Optional[str] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


def init_db(book_records: List[Dict], author_records: List[Dict]) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()

        # проверка наличия таблицы 'authors'
        cursor.execute(
            f"""
                    SELECT name FROM sqlite_master
                    WHERE type='table' AND name='{AUTHORS_TABLE_NAME}'
                    """
        )
        authors_exists = cursor.fetchone()

        # создание (если отсутствует) и заполнение данными таблицы 'authors'
        if not authors_exists:
            cursor.executescript(
                f"""
                        CREATE TABLE `{AUTHORS_TABLE_NAME}`(
                            author_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            first_name VARCHAR(50) NOT NULL,
                            last_name VARCHAR(50) NOT NULL,
                            middle_name VARCHAR(50)
                        );
                        """
            )
            cursor.executemany(
                f"""
                        INSERT INTO `{AUTHORS_TABLE_NAME}`
                        (author_id, first_name, last_name) VALUES (:author_id, :first_name, :last_name)
                        """, author_records
            )
        # проверка наличия таблицы 'books'
        cursor.execute(
            f"""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='{BOOKS_TABLE_NAME}';
            """
        )
        books_exists = cursor.fetchone()

        # создание (если отсутствует) и заполнение данными таблицы 'books'
        if not books_exists:
            cursor.executescript(
                f"""
                CREATE TABLE `{BOOKS_TABLE_NAME}`(
                    book_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title VARCHAR(50) NOT NULL ,
                    author_id INTEGER NOT NULL REFERENCES {AUTHORS_TABLE_NAME} (author_id) 
                        ON DELETE CASCADE 
                        ON UPDATE CASCADE 
                );
                """
            )
            cursor.executemany(
                f"""
                INSERT INTO `{BOOKS_TABLE_NAME}`
                (title, author_id) VALUES (:title, :author_id)
                """, book_records
            )


def _get_book_obj_from_row(row: tuple) -> Book:
    return Book(id=row[0], title=row[1], author_id=row[2])


def _get_author_obj_from_row(row: tuple) -> Author:
    return Author(id=row[0], first_name=row[1], last_name=row[2], middle_name=row[3])


def get_all_books() -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT *
            FROM {BOOKS_TABLE_NAME}
                """
        )
        all_books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in all_books]


def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE book_id = ?
            """,
            (book_id,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def add_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{BOOKS_TABLE_NAME}` 
            (title, author_id) VALUES (?, ?)
            """,
            (book.title, book.author_id)
        )
        book.id = cursor.lastrowid
        return book


def update_book_by_id(book: Book) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE {BOOKS_TABLE_NAME}
            SET title = ?, author_id = ?
            WHERE book_id = ?
            """,
            (book.title, book.author_id, book.id)
        )
        conn.commit()


def update_book_patch_by_id(book_id: int, book_data: dict):
    book_title = book_data.get('title')
    book_author_id = book_data.get('author_id')

    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()

        if all((book_title, book_author_id)):
            return update_book_by_id(Book(id=book_id, title=book_title, author_id=book_author_id))
        elif book_title is not None:
            cursor.execute(
                f"""
                            UPDATE {BOOKS_TABLE_NAME}
                            SET title = ?
                            WHERE book_id = ?
                            """,
                (book_title, book_id)
            )
            conn.commit()
        elif book_author_id is not None:
            cursor.execute(
                f"""
                UPDATE {BOOKS_TABLE_NAME}
                SET author_id = ?
                WHERE book_id = ?
                """,
                (book_author_id, book_id)
            )
            conn.commit()


def delete_book_by_id(book_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {BOOKS_TABLE_NAME}
            WHERE book_id = ?
            """,
            (book_id,)
        )
        conn.commit()


def get_book_by_title(book_title: str) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE title = ?
            """,
            (book_title,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def get_author_by_id(author_id: int) -> Optional[Author]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{AUTHORS_TABLE_NAME}` WHERE author_id = ?
            """,
            (author_id,)
        )
        author = cursor.fetchone()
        if author:
            return _get_author_obj_from_row(author)


def get_all_authors() -> Optional[List[Author]]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{AUTHORS_TABLE_NAME}`
            """
        )
        authors = cursor.fetchall()
        if authors:
            return [_get_author_obj_from_row(author) for author in authors]


def get_all_books_by_author(author_id: int) -> Optional[List[Book]]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT *
            FROM {BOOKS_TABLE_NAME}
            WHERE author_id = ?
                """,
            (author_id, )
        )
        all_books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in all_books]


def delete_author_by_id(author_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {AUTHORS_TABLE_NAME}
            WHERE author_id = ?
                """,
            (author_id, )
        )
        cursor.execute(
            f"""
                    DELETE FROM {BOOKS_TABLE_NAME}
                    WHERE author_id = ?
                        """,
            (author_id,)
        )
        conn.commit()


def add_author(author: Author):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()

        if author.middle_name is not None:
            cursor.execute(
                f"""
                            INSERT INTO {AUTHORS_TABLE_NAME} (first_name, last_name, middle_name)
                            VALUES (?, ?, ?)
                                """,
                (author.first_name, author.last_name, author.middle_name)
            )
        else:
            cursor.execute(
                f"""
                            INSERT INTO {AUTHORS_TABLE_NAME} (first_name, last_name)
                            VALUES (?, ?)
                                """,
                (author.first_name, author.last_name)
            )
        author.id = cursor.lastrowid
        return author


def is_author_exists(author: Author) -> bool:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()

        if author.middle_name is not None:
            cursor.execute(
                f"""
                SELECT * FROM {AUTHORS_TABLE_NAME}
                WHERE first_name = ? AND last_name = ? AND middle_name = ?
                        """,
                (author.first_name, author.last_name, author.middle_name)
            )
            if cursor.fetchone():
                return True
            return False
        else:
            cursor.execute(
                f"""
                            SELECT * FROM {AUTHORS_TABLE_NAME}
                            WHERE first_name = ? AND last_name = ?
                                    """,
                (author.first_name, author.last_name)
            )
            if cursor.fetchone():
                return True
            return False

def add_author_and_book(author: Author) -> Optional[Author]:
    author = add_author(author)
    book = Book(title=author.title, author_id=author.id)
    add_book(book)
    return author