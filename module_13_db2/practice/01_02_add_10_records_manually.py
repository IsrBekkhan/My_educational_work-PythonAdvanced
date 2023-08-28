import sqlite3


def add_10_records_to_table_warehouse(cursor: sqlite3.Cursor) -> None:
    products = [
        {'name': 'Кола', 'description': 'Холодный напиток', 'amount': 50},
        {'name': 'Fanta', 'description': 'Холодный напиток с апельсиновым вкусом', 'amount': 40},
        {'name': 'Помидоры', 'description': 'Свежие, позавчерашние', 'amount': 10},
        {'name': 'Яблоки', 'description': 'Сорт делишес', 'amount': 20},
        {'name': 'Груши', 'description': 'Зимние, синие', 'amount': 15},
        {'name': 'Кола', 'description': 'Холодный напиток', 'amount': 50},
        {'name': 'Fanta', 'description': 'Холодный напиток с апельсиновым вкусом', 'amount': 40},
        {'name': 'Помидоры', 'description': 'Свежие, позавчерашние', 'amount': 10},
        {'name': 'Яблоки', 'description': 'Сорт делишес', 'amount': 20},
        {'name': 'Груши', 'description': 'Зимние, синие', 'amount': 15},
    ]
    for elem in products:
        cursor.execute(
                """
            INSERT INTO 'table_warehouse' (name, description, amount) VALUES
                (?, ?, ?);
                """,
            (elem['name'], elem['description'], elem['amount'])
        )


if __name__ == "__main__":
    with sqlite3.connect("../materials/db_1.db") as conn:
        cursor = conn.cursor()
        add_10_records_to_table_warehouse(cursor)
        conn.commit()
