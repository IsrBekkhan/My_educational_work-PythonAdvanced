from sqlalchemy import Column, Integer, create_engine, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///mass_operations.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    # bulk_save_objects
    parent_1 = Parent(name="Nikita")
    parent_2 = Parent(name="Nastya")
    parent_3 = Parent(name="Vlad")
    parent_4 = Parent(name="Lera")

    session.bulk_save_objects([parent_1, parent_2, parent_3, parent_4])
    session.commit()

    parents = session.query(Parent).all()

    # bulk_insert_mappings
    insert_parents = [
        {"name": "Nikita2"},
        {"name": "Nastya2"},
        {"name": "Vlad2"},
        {"name": "Lera2"},
    ]
    session.bulk_insert_mappings(Parent, insert_parents)
    session.commit()

    parents = session.query(Parent).all()

    # bulk_update_mappings
    update_parents = [
        {"id": 1, "name": "Nikita_new"},
        {"id": 2, "name": "Nastya_new"},
    ]
    session.bulk_update_mappings(Parent, update_parents)
    session.commit()
    parents = session.query(Parent).all()