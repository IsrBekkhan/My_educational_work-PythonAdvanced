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
    parent_id = Column(ForeignKey("parent.id"), primary_key=True)
    child_id = Column(ForeignKey("child.id"), primary_key=True)
    extra_data = Column(String(50))
    child = relationship("Child", back_populates="parent")
    parent = relationship("Parent", back_populates="child")


class Parent(Base):
   __tablename__ = 'parent'
   id = Column(Integer, primary_key=True)
   children = relationship("Association", back_populates="parent")
   all_children = association_proxy('children', 'id')


class Child(Base):
   __tablename__ = 'child'
   id = Column(Integer, primary_key=True)
   parents = relationship("Association", back_populates="child")


if __name__ == '__main__':
   Base.metadata.create_all(bind=engine)

   father = Parent()
   mother = Parent()

   son = Child()
   daughter = Child()

   # добавим отцу детей
   # children - коллекция детей
   father.children.append(son)
   father.children.append(daughter)


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

   many_to_many_data = session.query(Association).all()

   father.children.remove(daughter)
   # как себя поведет интеграционная таблица?
   session.delete(son)