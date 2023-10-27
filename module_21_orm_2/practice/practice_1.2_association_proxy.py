from sqlalchemy import Column, Integer, ForeignKey, create_engine, Table, String
from sqlalchemy.orm import relationship, sessionmaker, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

engine = create_engine('sqlite:///many_to_many.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Association(Base):
    __tablename__ = "association_table"
    left_id = Column(ForeignKey("left_table.id"), primary_key=True)
    right_id = Column(ForeignKey("right_table.id"), primary_key=True)
    extra_data = Column(String(50))

    # ссылается на правую часть посредством отношения «многие к одному»
    child = relationship("Child", back_populates="parents")
    parent = relationship("Parent", back_populates="children")


class Parent(Base):
    __tablename__ = "left_table"
    id = Column(Integer, primary_key=True)

    # ссылается на объект Association посредством отношения «один ко многим»
    children = relationship("Association", back_populates="parent")
    all_children = association_proxy('children', 'right_id')


class Child(Base):
    __tablename__ = "right_table"
    id = Column(Integer, primary_key=True)
    parents = relationship("Association", back_populates="child")


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    # создаем родителя, добавляем дочернего элемента через ассоциацию
    p = Parent()
    a = Association(extra_data="some data")
    a.child = Child()
    p.children.append(a)

    # итерировать дочерние объекты через ассоциацию, включая атрибуты ассоциации
    for assoc in p.children:
        print(assoc.extra_data)
        print(assoc.child)