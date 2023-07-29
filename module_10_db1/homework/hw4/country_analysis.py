import sqlite3


if __name__ == '__main__':

    with (sqlite3.connect('hw_4_database.db') as connect):
        cursor = connect.cursor()

        # решение задачи 1
        cursor.execute("SELECT COUNT(*) people_count "
                       "FROM salaries "
                       "WHERE salary < 5000")
        result = cursor.fetchone()
        print('4.1. Количество людей с доходом ниже 5000 гульденов:', result[0])

        # решение задачи 2
        cursor.execute("SELECT ROUND(AVG(salary), 2) FROM salaries")
        result = cursor.fetchone()
        print('4.2. Средняя зарплата:', result[0])

        # решение задачи 3
        people_count = "SELECT COUNT(*) FROM salaries"
        half_count = "SELECT COUNT(*) / 2 FROM salaries"
        table_half_if_even = f"SELECT salary FROM salaries LIMIT ({half_count}) - 1, 2"
        table_half_if_odd = f"SELECT salary FROM salaries LIMIT ({half_count}) - 1, 1"

        query = (f"SELECT IIF (({people_count}) % 2 == 0, "
                 f"(SELECT SUM(salary) / 2 FROM ({table_half_if_even})), "
                 f"(SELECT salary FROM ({table_half_if_odd})))")

        cursor.execute(query)
        median = cursor.fetchone()[0]

        print('4.3. Медианная зарплата:', median)

        # 4. Посчитать число социального неравенства F, определяемое как `F = T/K`,
        # где `T` — суммарный доход 10% самых обеспеченных жителей острова `N, K` — суммарный доход остальных 90% людей.
        # Вывести ответ в процентах с точностью до двух знаков после запятой.

        # В один SQL-запрос

        PERCENT_10 = 'SELECT 0.1 * COUNT(*) FROM salaries'
        T_salaries = f'SELECT salary FROM salaries ORDER BY salary DESC LIMIT ({PERCENT_10})'
        T_sum = f'SELECT SUM(salary) FROM ({T_salaries})'
        T = f'CAST(({T_sum}) AS FLOAT)'

        PERCENT_90 = 'SELECT 0.9 * COUNT(*) FROM salaries'
        K_salaries = f'SELECT salary FROM salaries ORDER BY salary LIMIT ({PERCENT_90})'
        K_sum = f'SELECT SUM(salary) FROM ({K_salaries})'
        K = f'CAST(({K_sum}) AS FLOAT)'

        F = f'SELECT ROUND(100 * {T} / {K}, 2) as percent'
        cursor.execute(F)

        result, *_ = cursor.fetchone()
        print('4.4. Число социального неравенства, %:', result)



