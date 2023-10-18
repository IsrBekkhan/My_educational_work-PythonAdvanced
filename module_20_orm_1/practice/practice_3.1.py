from sqlalchemy import MetaData, Table, Column, Integer, String, create_engine, text
from sqlalchemy.orm import mapper, sessionmaker


engine = create_engine('sqlite:///sqlite_python.db')
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()

users = Table('user', metadata,
             Column('id', Integer, primary_key=True),
             Column('name', String(16), nullable=False),
             Column('email', String(60)),
             Column('login', String(50), nullable=False)
             )


class User(object):
   def __init__(self, name, email, login):
       self.name = name
       self.email = email
       self.login = login

   def __repr__(self):
       return f"{self.name}, {self.email}, {self.login}"


mapper(User, users)
metadata.create_all(bind=engine)

t = text("SELECT * FROM users WHERE id=:user_id")

result = session.execute(t, params={'user_id': 1})
print(result.one())

