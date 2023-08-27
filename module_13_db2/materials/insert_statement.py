import sqlite3


class AddingItem:
    def __init__(self, name: str, year: int) -> None:
        self.name: str = name
        self.amount: int = year


def input_new_item() -> AddingItem:
    name: str = input("Введите имя\n>")
    year: str = input("Введите возраст\n>")

    amount_val: int = int(year)

    return AddingItem(name=name, year=amount_val)


if __name__ == "__main__":
    with sqlite3.connect("../practice/sample_database.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        new_item: AddingItem = input_new_item()

        cursor.execute(
            """
            INSERT INTO `table_people` (name, year) VALUES 
                (?, ?);
            """,
            (new_item.name, new_item.amount),
        )
        conn.commit()
