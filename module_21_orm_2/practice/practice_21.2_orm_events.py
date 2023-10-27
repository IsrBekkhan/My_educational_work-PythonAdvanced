from sqlalchemy import Column, Integer, String, create_engine, event
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from sqlalchemy.engine.base import Connection

Base = declarative_base()
engine = create_engine('sqlite:///example.db')
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

    @validates('age')
    def validate_age(self, key, age):
        assert age > 0, 'Age must be a positive number'
        return age

def on_user_save(mapper: mapper, connection: Connection, target: User):
    print(f"User {target.name} is being saved")
    print(mapper)
    print(connection)

    print(target.id, target.name, target.age)
    target.age = 30


Base.metadata.create_all(engine)

# Регистрируем обработчик события save для модели User
event.listen(User, 'before_insert', on_user_save)

# Создаем и сохраняем пользователя
user = User(name='Alice', age=25)
session.add(user)
session.commit()

# # Затем можно обновить пользователя
# user.age = 30
# session.commit()
#
# # И наконец удалить пользователя
# session.delete(user)
# session.commit()