from sqlalchemy import Column, Integer, create_engine, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///flush.db', echo=True)
Session = sessionmaker(bind=engine, autoflush=False)
session = Session()
Base = declarative_base()


class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    parent = Parent(name="Nikita")
    session.add(parent)

    q_1 = session.query(Parent).all()
    print('q1')
    session.commit()

    new_session = Session()
    new_session.autoflush = False

    new_session.add(Parent(name="Vlad"))
    q_2 = new_session.query(Parent).all()
    print('q2')
    new_session.flush()

    q3 = new_session.query(Parent).all()
    print('q3')

    # другая сессия не видит
    q4 = session.query(Parent).all()
    print('q4')

    new_session.rollback()

    q5 = new_session.query(Parent).all()

    print('q5')

    parent = Parent()
    session.add(parent)
    session.flush()
    id = parent.id
    #child = Child(parent_id=id)
    session.commit()