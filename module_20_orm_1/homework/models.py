from sqlalchemy import create_engine, Column, Integer, String, Date, Float, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from datetime import datetime, timedelta

from typing import Dict, Any, List


engine = create_engine('sqlite:///sqlite_library.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, nullable=False)

    def to_json(self) -> Dict[str, Any]:
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}

    @classmethod
    def all_books(cls) -> List[dict]:
        books = session.query(Book).all()
        return [book.to_json() for book in books]

    @classmethod
    def get_book_by_title(cls, title: str):
        result = session.query(Book).filter(
            Book.name.like(f'%{title}%') |
            Book.name.like(f'%{title}') |
            Book.name.like(f'{title}%')
        ).one_or_none()
        session.close()
        return result



class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    surname = Column(String(20), nullable=False)

    def to_json(self) -> Dict[str, Any]:
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    surname = Column(String(20), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(30), nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    def to_json(self) -> Dict[str, Any]:
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}

    @classmethod
    def get_all_students_with_scholarship(cls):
        return session.query(Student).filter(Student.scholarship is True).all()

    @classmethod
    def average_score_more_students(cls, score):
        return session.query(Student).filter(Student.average_score > score).all()


class ReceivingBook(Base):
    __tablename__ = 'receiving_books'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime)

    def to_json(self) -> Dict[str, Any]:
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}

    @hybrid_property
    def count_date_with_book(self):
        if self.date_of_return is not None:

            if self.date_of_return > datetime.now():
                delta: timedelta = self.date_of_return - datetime.now()
                return delta.days

            delta: timedelta = self.date_of_return - self.date_of_issue
            return delta.days

    @classmethod
    def all_debtors(cls) -> List[dict]:
        debtors = session.query(ReceivingBook).filter(ReceivingBook.count_date_with_book > 14).all()
        return [debtor.to_json() for debtor in debtors]

    @classmethod
    def add_line(cls, book_id: int, student_id: int):
        date_of_issue = datetime.now()
        new_line = ReceivingBook(
                book_id=book_id,
                student_id=student_id,
                date_of_issue=date_of_issue
        )
        session.add(new_line)
        session.commit()
        result = session.query(ReceivingBook).filter(ReceivingBook.id == new_line.id).one()
        session.close()
        return result

    @classmethod
    def delete_line(cls, book_id: int, student_id: int):
        deleter_line = session.query(ReceivingBook).filter(
            ReceivingBook.book_id == book_id,
            ReceivingBook.student_id == student_id
        ).all()
        if deleter_line:
            session.delete(deleter_line[0])
            all_lines = session.query(ReceivingBook).all()
            result = [line.to_json() for line in all_lines]
            session.commit()
            session.close()
            return result

        session.close()
        return f'Ошибка: записи с book_id = {book_id} и student_id = {student_id} не существует!'


if __name__ == '__main__':
    result_ = session.query(ReceivingBook).filter(ReceivingBook.count_date_with_book < 10).one()

