import sqlite3
import csv


def add_books_from_file(c: sqlite3.Cursor, file_name: str) -> None:
    with open('book_list.csv', 'r', encoding='utf-8') as book_file:
        csv_reader = csv.DictReader(book_file, delimiter=',')

        for book in csv_reader:
            isbn, book_name, author, year = book['isbn'], book['book_name'], book['author'], book['year']
            cursor.execute(
                """
            INSERT INTO 'table_warehouse' (name, description, amount) VALUES
                (?, ?, ?);
                """,
                (book_name, author + ' --- ' + isbn, year)
            )



if __name__ == "__main__":
    with sqlite3.connect("../materials/db_1.db") as conn:
        cursor = conn.cursor()
        add_books_from_file(cursor, "book_list.csv")
        conn.commit()
