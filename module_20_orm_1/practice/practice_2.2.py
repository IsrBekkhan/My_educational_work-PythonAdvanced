from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///sqlite_python.db')

# создание конфигурации класса Session
Session = sessionmaker(bind=engine)

# создание объекта Session
session = Session()
t = text("SELECT * FROM users WHERE id=:user_id")

result = session.execute(t, params={'user_id': 1})
print(result.all())