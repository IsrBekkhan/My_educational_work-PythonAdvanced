from sqlalchemy import Column, Integer, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker, backref
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///one_to_one.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Parent(Base):
   __tablename__ = 'parent'
   id = Column(Integer, primary_key=True)
   # children = relationship("Child", back_populates="parent")

   # преобразуем в скалярную связь один к одному
   child = relationship("Child", back_populates="parent", uselist=False)


class Child(Base):
   __tablename__ = 'child'
   id = Column(Integer, primary_key=True)
   parent_id = Column(Integer, ForeignKey('parent.id'), unique=True)
   # parent = relationship("Parent", back_populates="children")

   # переименуем back_populates
   parent = relationship("Parent", back_populates="child")

   # определение с помощью backref
   # parent = relationship("Parent",
   #                       backref=backref("child", uselist=False))


if __name__ == '__main__':
   Base.metadata.create_all(bind=engine)
   parent = Parent()
   session.add(parent)
   session.commit()
   child_one = Child(parent_id=1)
   session.add(child_one)
   session.commit()

   # child_two = Child(parent_id=1)
   # session.add(child_two)
   # session.commit()

   # проверить родителя
   check_parent = session.query(Parent).filter_by(id=1).one()
   print('check')

   # проверим детей (дети привязываются к родителю все равно)
   children = session.query(Child).all()
   print('check')