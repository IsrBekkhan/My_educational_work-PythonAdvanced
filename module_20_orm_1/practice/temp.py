from sqlalchemy import create_engine, Column, Integer, String, Date, Float, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from datetime import datetime, timedelta

from typing import Dict, Any, List

from random import randint


engine = create_engine('sqlite:///sqlite_library.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Test(Base):
    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True)
    start = Column(Integer, nullable=False)
    end = Column(Integer, nullable=False)

    def to_json(self) -> Dict[str, Any]:
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}

    @hybrid_property
    def length(self):
        return self.end - self.start

    @classmethod
    def all_lines(cls) -> List[dict]:
        lines = session.query(Test).all()
        return [line.to_json() for line in lines]

    @classmethod
    def add_line(cls):
        a = randint(10, 1000)
        b = randint(10, 1000)
        session.add(Test(start=a, end=b))
        session.commit()
        session.close()

if __name__ == '__main__':
    #Base.metadata.create_all(engine)
    #print(Test.add_line())
    result = session.query(Test.length).filter(Test.length < 0).all()
    print(result)
