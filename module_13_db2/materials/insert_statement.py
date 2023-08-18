import sqlite3


class AddingItem:
    def __init__(self, name: str, description: str, amount: int) -> None:
        self.name: str = name
        self.description: str = description
        self.amount: int = amount


def input_new_item() -> AddingItem:
    name: str = input("Введите имя продукта\n>")
    description: str = input("Введите описание продукта\n>")
    amount: str = input("Введите остаток на складе\n>")

    amount_val: int = int(amount)

    return AddingItem(name=name, description=description, amount=amount_val)


if __name__ == "__main__":
    with sqlite3.connect("db_1.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        new_item: AddingItem = input_new_item()

        cursor.execute(
            """
            INSERT INTO `table_warehouse` (name, description, amount) VALUES 
                (?, ?, ?);
            """,
            (new_item.name, new_item.description, new_item.amount),
        )
        conn.commit()
