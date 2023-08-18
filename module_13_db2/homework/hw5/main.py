import sqlite3


def generate_test_data(
        cursor: sqlite3.Cursor,
        number_of_groups: int
) -> None:
    ...


if __name__ == '__main__':
    number_of_groups: int = int(input('Введите количество групп (от 4 до 16): '))
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        generate_test_data(cursor, number_of_groups)
        conn.commit()
