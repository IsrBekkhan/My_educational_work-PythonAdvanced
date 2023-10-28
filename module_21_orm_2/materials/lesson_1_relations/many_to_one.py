from sqlalchemy import Column, Integer, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///many_to_one.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('child.id'))
    child = relationship("Child")
    # двунаправленная связь
    # child = relationship("Child", back_populates="parents")
    # альтернативый вариант двунаправленной связи
    # child = relationship("Child", backref="parents")


class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    # двунаправленная связь
    # parents = relationship("Parent", back_populates="child")


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    child = Child()
    session.add(child)
    session.commit()
    mother = Parent(child_id=1)
    father = Parent(child_id=1)
    session.add(mother)
    session.add(father)
    session.commit()

    parents = session.query(Parent).filter(Parent.child_id == 1).all()
    child = session.query(Child).first()