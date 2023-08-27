import sqlite3
from random import choice
from teams import hard_teams, medium_teams, weak_teams

delete_commands_request = """
DELETE FROM uefa_commands
"""

delete_draw_request = """
DELETE FROM uefa_draw
"""

insert_teams_request = """
INSERT INTO uefa_commands(command_name, command_country, command_level)
    VALUES (:name, :country, :level)
"""

insert_groups_request = """
INSERT INTO uefa_draw(command_number, group_number)
    VALUES (:number, :group)
"""


def generate_test_data(
        cursor_: sqlite3.Cursor,
        number_of_groups_: int
) -> None:
    cursor_.execute(delete_commands_request)

    teams_data = list()

    for group in range(1, number_of_groups_ + 1):
        hard_team = choice(hard_teams)
        hard_teams.remove(hard_team)
        teams_data.append({'name': hard_team[0], 'country': hard_team[1], 'level': 'hard_team', 'group': group})

        medium_team_1 = choice(medium_teams)
        medium_teams.remove(medium_team_1)
        teams_data.append({'name': medium_team_1[0], 'country': medium_team_1[1], 'level': 'medium_team', 'group': group})

        medium_team_2 = choice(medium_teams)
        medium_teams.remove(medium_team_2)
        teams_data.append({'name': medium_team_2[0], 'country': medium_team_2[1], 'level': 'medium_team', 'group': group})

        weak_team = choice(weak_teams)
        weak_teams.remove(weak_team)
        teams_data.append({'name': weak_team[0], 'country': weak_team[1], 'level': 'weak_team', 'group': group})

    cursor_.executemany(insert_teams_request, teams_data)

    draw_data = [{'number': number + 1, 'group': elem['group']} for number, elem in enumerate(teams_data)]

    cursor_.execute(delete_draw_request)
    cursor_.executemany(insert_groups_request, draw_data)
    print('Жеребьёвка завершена!')



if __name__ == '__main__':
    number_of_groups: int = int(input('Введите количество групп (от 4 до 16): '))

    if 16 < number_of_groups or number_of_groups < 4:
        print('Вы ввели некорректное число групп.')
    else:
        with sqlite3.connect('../homework.db') as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            generate_test_data(cursor, number_of_groups)
            conn.commit()
