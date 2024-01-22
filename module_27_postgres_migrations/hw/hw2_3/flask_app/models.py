from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Boolean, JSON, ARRAY, \
    select, func
from sqlalchemy.orm import relationship

from database import Base, session

from typing import Dict, Any, List


class Coffee(Base):
    __tablename__ = 'coffee'

    id = Column(Integer, Sequence('coffee_id_seq'), primary_key=True)
    title = Column(String(200), nullable=False)
    origin = Column(String(200))
    intensifier = Column(String(100))
    notes = Column(ARRAY(String))

    def to_json(self) -> Dict[str, Any]:
        return {
            c.name: getattr(self, c.name) for c in self.__table__.columns
        }

    @classmethod
    def check_coffee(cls, coffee_id: int) -> bool:
        coffee = session.query(Coffee).filter(Coffee.id == coffee_id)
        if coffee.one_or_none() is None:
            return False
        return True

    @classmethod
    def get_coffee(cls, coffee_name: str) -> List:
        result = session.execute(
            select(Coffee).where(Coffee.title.match(coffee_name))
        )
        coffe_list = result.unique().scalars().all()
        return [coffee.to_json() for coffee in coffe_list]

    @classmethod
    def get_distinct_notes(cls) -> List[str]:

        all_notes_query = select(func.unnest(Coffee.notes).label('notes')).subquery()
        distinct_notes_query = select(func.distinct(all_notes_query.c.notes).label('distinct_notes')).subquery()
        main_query = select(func.array_agg(distinct_notes_query.c.distinct_notes))
        result = session.execute(main_query)

        return result.scalars().one()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=True)
    patronomic = Column(String(50), nullable=True)
    # has_sale = Column(Boolean())
    address = Column(JSON)
    coffee_id = Column(Integer, ForeignKey('coffee.id'))

    coffee = relationship('Coffee',
                          cascade='all',
                          lazy='select')

    def to_json(self) -> Dict[str, Any]:
        return {
            c.name: getattr(self, c.name) for c in self.__table__.columns
        }

    @classmethod
    def add_user(cls, user: 'User') -> dict:
        user = User(**user.to_json())
        session.add(user)
        session.commit()

        user_dict = user.to_json()
        user_dict['coffee'] = user.coffee.to_json()
        return user_dict

    @classmethod
    def get_users_from(cls, country: str) -> List['User']:
        query = select(User).where(User.address['country'].as_string().match(country))
        result = session.execute(query)
        return [user.to_json() for user in result.scalars().all()]
