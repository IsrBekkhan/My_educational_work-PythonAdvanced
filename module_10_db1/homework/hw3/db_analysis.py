import sqlite3


if __name__ == '__main__':

    with sqlite3.connect('hw_3_database.db') as connect:
        cursor = connect.cursor()

        for i in range(1, 4):
            cursor.execute(f"SELECT COUNT(*) count FROM 'table_{i}'")
            result = cursor.fetchone()

            print(f'Количество записей в table_{i}: {result[0]}')

        cursor.execute("SELECT COUNT(DISTINCT id) unique_count FROM table_1")
        result = cursor.fetchone()
        print('\nКоличество уникальных записей в table_1:', result[0])

        cursor.execute("SELECT COUNT(*) 'count' "
                       "FROM table_1 t1 "
                       "JOIN table_2 t2 ON t1.id = t2.id and t1.value = t2.value")
        result = cursor.fetchone()
        print('\nКоличество записей из table_1, встречающиеся в table_2:', result[0])

        cursor.execute("SELECT COUNT(*) 'count' "
                       "FROM table_1 t1 "
                       "JOIN table_2 t2 ON t1.id=t2.id and t1.value=t2.value "
                       "JOIN table_3 t3 ON t1.id=t3.id and t1.value=t3.value")
        result = cursor.fetchone()
        print('\nКоличество записей из table_1, встречающиеся в table_2 и в table_3:', result[0])