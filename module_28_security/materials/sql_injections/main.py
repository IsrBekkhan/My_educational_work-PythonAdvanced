import json
import sqlite3

from flask import Flask, request, g

create_db_sql = """
DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   username VARCHAR(255) NOT NULL,
   role VARCHAR(255) NOT NULL
);
"""

app = Flask(__name__)

def get_db():
   db = getattr(g, '_database', None)
   if db is None:
       db = g._database = sqlite3.connect("db_users.db")
   return db


@app.teardown_appcontext
def close_connection(exception):
   db = getattr(g, '_database', None)
   if db is not None:
       db.close()


def create_db():
   with sqlite3.connect("db_users.db") as conn:
       cursor = conn.cursor()
       cursor.executescript(create_db_sql)


@app.route('/users')
def get_users():
   conn = get_db()
   cursor: sqlite3.Cursor = conn.cursor()
   cursor.execute("SELECT * FROM users")
   users = cursor.fetchall()
   return json.dumps(users)


@app.route('/users', methods=['POST'])
def create_user():
   data = request.get_json()
   conn = get_db()
   cursor: sqlite3.Cursor = conn.cursor()
   cursor.execute(
       f"""
           INSERT INTO
               `users`(username, role)
           VALUES
               (?, ?);
       """,
       (
           data['username'],
           data['role'],
       ),
   )
   conn.commit()
   return 'OK', 200


if __name__ == '__main__':
   create_db()
   app.run(debug=True)
