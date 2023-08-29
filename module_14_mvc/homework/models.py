import sqlite3
from typing import Any, Optional, List, Tuple

DATA: List[dict] = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 'Swaroop C. H.', 'counter': 0},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville', 'counter': 0},
    {'id': 3, 'title': 'War and Peace', 'author': 'Leo Tolstoy', 'counter': 0},
]


class Book:

    def __init__(self, id: int, title: str, author: str, counter: int) -> None:
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.counter: int = counter

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


def init_db(initial_records: List[dict]) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='table_books'; 
            """
        )
        exists: Optional[tuple[str,]] = cursor.fetchone()
        # now in `exist` we have tuple with table name if table really exists in DB
        if not exists:
            cursor.executescript(
                """
                CREATE TABLE `table_books` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT, 
                    author TEXT,
                    counter INTEGER
                )
                """
            )
            cursor.executemany(
                """
                INSERT INTO `table_books`
                (title, author, counter) VALUES (?, ?, ?)
                """,
                [
                    (item['title'], item['author'], item['counter'])
                    for item in initial_records
                ]
            )


def get_all_books() -> List[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * from `table_books`
            """
        )
        all_books = cursor.fetchall()

        if all_books:
            counter_up(cursor, all_books)

        return [Book(*row) for row in all_books]


def add_new_book(title: str, author: str) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO 'table_books'(title, author)
                VALUES (?, ?)
            """,
            (title, author)
        )


def get_authors_books(author: str) -> List[tuple]:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT title, author FROM table_books
                WHERE author LIKE ?
            """,
            ('%' + author + '%', )
        )
        authors_books = cursor.fetchall()

        if authors_books:
            counter_up(cursor, authors_books)

        return authors_books


def counter_up(cursor: sqlite3.Cursor, books_list: List) -> None:

    if len(books_list[0]) == 4:
        books_id = [{'id': book[0]} for book in books_list]
        cursor.executemany(
            """
            UPDATE table_books
                SET counter = (
                        SELECT counter FROM table_books
                        WHERE id = :id
                        ) + 1
                WHERE id = :id
            """,
            books_id
        )
    else:
        books_id = [{'title': book[0]} for book in books_list]
        cursor.executemany(
            """
            UPDATE table_books
                SET counter = (
                        SELECT counter FROM table_books
                        WHERE title = :title
                        ) + 1
                WHERE title = :title
            """,
            books_id
        )


def get_book_info(book_id: int) -> Tuple:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM table_books
                WHERE id = ?
            """,
            (book_id, )
        )
        book_info = cursor.fetchall()

        if book_info:
            counter_up(cursor, book_info)
            return book_info[0]