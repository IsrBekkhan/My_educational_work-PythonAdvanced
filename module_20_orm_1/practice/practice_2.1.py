if __name__ == '__main__':
    from sqlalchemy import text, create_engine
    engine = create_engine('sqlite:///sqlite_python.db')

    with engine.connect() as connection:
        create_user_table_q = """
        CREATE TABLE IF not EXISTS users (
        id integer PRIMARY KEY,
        name text NOT NULL) 
        """

        connection.execute(create_user_table_q)
        connection.execute("""INSERT INTO users (name)
                        values('Nikita')""")

        t = text("SELECT * FROM users WHERE id=:user_id")

        # это специальный объект который делает  запросы и получает их результаты
        cursor = connection.execute(t, user_id=1)
        result = cursor.fetchone()
        print(result)


