import sqlite3


sql_request = """
SELECT COUNT(*) 
    FROM 'table_kotlin' 
    WHERE wind >= ?; 
"""

def hurricane_counter(cursor_: sqlite3.Cursor, wind: int) -> int:
    cursor_.execute(sql_request, (wind, ))
    return cursor_.fetchone()[0]

if __name__ == '__main__':
    with sqlite3.connect('practise.db') as connect:
        cursor = connect.cursor()
        result = hurricane_counter(cursor, 10)
        print(f'Количество ураганных дней над островом Котлин за всю историю наблюдения: {result}')