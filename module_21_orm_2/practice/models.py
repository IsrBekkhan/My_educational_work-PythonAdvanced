from sqlalchemy import (create_engine, func,
                        Column, ForeignKey, UniqueConstraint,
                        Integer, String, Date, Float, Boolean, DateTime
                        )
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, backref, joinedload
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
import sqlalchemy

from datetime import datetime, timedelta
from typing import Dict, Any, List


engine = create_engine('sqlite:///sqlite_library.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)

    author = relationship('Author', backref=backref('books',
                                                    cascade="all, delete-orphan",
                                                    lazy='select'))
    student_association = relationship('ReceivingBook',
                                       back_populates='book',
                                       cascade="all, delete-orphan",
                                       lazy='joined')
    students = association_proxy('student_association', 'student')

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
    UniqueConstraint(name, surname, name='full_name')

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

    book_association = relationship('ReceivingBook',
                                    back_populates='student',
                                    cascade="save-update",
                                    lazy='subquery')
    books = association_proxy('book_association', 'book')

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

    book_id = Column(Integer, ForeignKey('books.id'), nullable=False,
                     primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=True,
                        primary_key=True)
    date_of_issue = Column(DateTime, nullable=False, default=datetime.now())
    date_of_return = Column(DateTime)

    book = relationship('Book', back_populates='student_association')
    student = relationship('Student', back_populates='book_association')


    def to_json(self) -> Dict[str, Any]:
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}

    @hybrid_property
    def count_date_with_book(self):
        end_date = self.date_of_return or datetime.now()
        return (end_date - self.date_of_issue).days

    @count_date_with_book.expression
    def count_date_with_book(cls):
        """
        Количество дней, которое читатель держит/держал книгу у себя
        """
        end_date = sqlalchemy.case(
            (cls.date_of_return == None, sqlalchemy.func.now()),
            else_=cls.date_of_return
        )
        return sqlalchemy.func.julianday(end_date) - sqlalchemy.func.julianday(cls.date_of_issue)

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


def insert_data():
    from datetime import date, datetime

    authors = [Author(name="Александр", surname="Пушкин"),
               Author(name="Лев", surname="Толстой"),
               Author(name="Михаил", surname="Булгаков"),
               ]

    authors[0].books.extend([Book(title="Капитанская дочка",
                                  count=5,
                                  release_date=date(1836, 1, 1)),
                             Book(title="Евгений Онегин",
                                  count=3,
                                  release_date=date(1838, 1, 1))
                             ])
    authors[1].books.extend([Book(title="Война и мир",
                                  count=10,
                                  release_date=date(1867, 1, 1)),
                             Book(title="Анна Каренина",
                                  count=7,
                                  release_date=date(1877, 1, 1))
                             ])
    authors[2].books.extend([Book(title="Морфий",
                                  count=5,
                                  release_date=date(1926, 1, 1)),
                             Book(title="Собачье сердце",
                                  count=3,
                                  release_date=date(1925, 1, 1))
                             ])

    students = [Student(name="Nik", surname="1", phone="2", email="3",
                        average_score=4.5,
                        scholarship=True),
                Student(name="Vlad", surname="1", phone="2", email="3",
                        average_score=4,
                        scholarship=True),
                ]
    session.add_all(authors)
    session.add_all(students)
    session.commit()


def give_me_book():
    nikita = session.query(Student).filter(Student.name == 'Nik').one()
    vlad = session.query(Student).filter(Student.name == 'Vlad').one()
    books_to_nik = session.query(Book).filter(Author.surname == 'Толстой',
                                              Author.id == Book.author_id).all()
    books_to_vlad = session.query(Book).filter(Book.id.in_([1, 3, 4])).all()

    for book in books_to_nik:
        receiving_book = ReceivingBook()
        receiving_book.book = book
        receiving_book.student = nikita
        session.add(receiving_book)

    for book in books_to_vlad:
        receiving_book = ReceivingBook()
        receiving_book.book = book
        receiving_book.student = vlad
        session.add(receiving_book)

    session.commit()


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    check_exist = session.query(Author).all()
    if not check_exist:
        insert_data()
        give_me_book()

    # subquery
    author_q = session.query(Author.id).filter_by(name='Лев').subquery()
    books_by_lev = session.query(Book) \
        .filter(Book.author_id.in_(author_q)).all()

    # labels
    students = session.query(Student.name.label('student_name')).all()
    for s in students:
        if s.student_name == 'Nik':
            print('Nik')

    # получим количество всех книг в библиотеке с помощью func.sum
    count_of_books = session.query(func.sum(Book.count)).scalar()

    # получим кол-во книг по каждому автору с помощью group_by
    # отсортированных по кол-ву по убыванию
    count_books_by_authors = session.query(func.sum(Book.count),
                                           Author.name,
                                           Author.surname) \
        .filter(Book.author_id == Author.id) \
        .group_by(Author.id).order_by(func.sum(Book.count).desc()) \
        .all()

    # использование joinedload - альтернатива lazy = 'joined' для объекта Query
    # Получаем книги со связанными авторами - жадная загрузка
    books_with_authors = session.query(Book).options(joinedload(
        Book.author)).all()

    import csv

    # join двух таблиц
    book_join_author = session.query(Book, Author).join(Book.author).all()

    # join subquery
    author_q = session.query(Author).filter_by(name='Михаил').subquery()
    michail_books = session.query(Book) \
        .join(author_q, Book.author_id == author_q.c.id) \
        .all()

    my_student: Student = session.query(Student).filter(Student.id == 1).one()
    print('-'*100)
    print(my_student.book_association)
    print(my_student.books)

    for book in my_student.book_association:
        print(book.book.title)

    for book in my_student.books:
        print(book.title)





