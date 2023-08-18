import sqlite3


def add_books_from_file(c: sqlite3.Cursor, file_name: str) -> None:
    ...


if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        add_books_from_file(cursor, "book_list.csv")
        conn.commit()
