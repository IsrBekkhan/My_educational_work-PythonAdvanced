import sqlite3


if __name__ == '__main__':

    with sqlite3.connect('hw_4_database.db') as connect:
        cursor = connect.cursor()

        # решение задачи 1
        cursor.execute("SELECT COUNT(*) people_count "
                       "FROM salaries "
                       "WHERE salary < 5000")
        result = cursor.fetchone()
        print('Количество людей с доходом ниже 5000 гульденов:', result[0])

        # решение задачи 2
        cursor.execute("SELECT ROUND(AVG(salary), 2) FROM salaries")
        result = cursor.fetchone()
        print('Средняя зарплата:', result[0])

        # решение задачи 3
        cursor.execute("SELECT COUNT(*) FROM salaries")
        people_count = cursor.fetchone()[0]

        if people_count % 2 == 0:
            cursor.execute(f"SELECT salary FROM salaries LIMIT {(people_count/2) - 1}, 2")
            result = [elem[0] for elem in cursor.fetchall()]
            median_salary = sum(result)/2

        else:
            cursor.execute(f"SELECT salary FROM salaries LIMIT {(people_count/2) - 1}, 1")
            median_salary = cursor.fetchone()

        print('Медианная зарплата:', median_salary)

        # решение задачи 4
        cursor.execute("SELECT SUM(salary) FROM ("
                       "SELECT salary FROM salaries "
                       "ORDER BY salary DESC "
                       "LIMIT (SELECT COUNT(*) FROM salaries) * 0.1)")
        T = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(salary) FROM ("
                       "SELECT salary FROM salaries "
                       "ORDER BY salary "
                       "LIMIT (SELECT COUNT(*) FROM salaries) * 0.9)")
        K = cursor.fetchone()[0]

        print('Число социального неравенства:', round(T / K, 2))

