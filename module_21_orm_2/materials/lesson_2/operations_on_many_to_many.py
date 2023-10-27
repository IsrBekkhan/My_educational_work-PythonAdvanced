from sqlalchemy import Column, Integer, ForeignKey, create_engine, Table
from sqlalchemy.orm import relationship, sessionmaker, backref
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///many_to_many.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

integration_table = Table('integrations', Base.metadata,
                         Column('parent_id', ForeignKey('parent.id'),
                                primary_key=True),
                         Column('child_id', ForeignKey('child.id'),
                                primary_key=True)
                         )


class Parent(Base):
   __tablename__ = 'parent'
   id = Column(Integer, primary_key=True)
   # children = relationship("Child",
   #                         secondary=integration_table)

   # двунаправленная связь
   children = relationship(
       "Child",
       secondary=integration_table,
       back_populates="parents")

   # определение с помощью backref
   # children = relationship("Child",
   #                         secondary=integration_table,
   #                         backref="parents")


class Child(Base):
   __tablename__ = 'child'
   id = Column(Integer, primary_key=True)

   # двунаправленная связь
   parents = relationship(
       "Parent",
       secondary=integration_table,
       back_populates="children")


if __name__ == '__main__':
   Base.metadata.create_all(bind=engine)

   father = Parent()
   mother = Parent()

   son = Child()
   daughter = Child()

   # добавим отцу детей
   # children - коллекция детей
   father.children.extend([son, daughter])


   # обратная ситуация - добавим сын и дочери маму (при двунаправленной связи)
   son.parents.append(mother)
   daughter.parents.append(mother)

   session.add(father)
   session.add(mother)
   session.add(son)
   session.add(daughter)
   session.commit()

   my_parents = session.query(Parent).all()
   my_children = session.query(Child).all()

   many_to_many_data = session.query(integration_table).all()

   father.children.remove(daughter)
   # как себя поведет интеграционная таблица?
   # session.delete(son)
   my_parents = session.query(Parent).all()
   my_children = session.query(Child).all()
   many_to_many_data = session.query(integration_table).all()
   print()