import csv

from sqlalchemy import (create_engine, func,
                        Column, ForeignKey, UniqueConstraint,
                        Integer, String, Date, Float, Boolean, DateTime
                        )
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
import sqlalchemy
from sqlalchemy import event

from sqlalchemy.exc import IntegrityError

from datetime import datetime, date
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
                                       lazy='select')
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
            Book.title.like(f'%{title}%') |
            Book.title.like(f'%{title}') |
            Book.title.like(f'{title}%')
        ).one_or_none()
        session.close()
        return result

    @classmethod
    def get_books_count_by_author_id(cls, author_id: int):
        count = session.query(func.sum(Book.count)).filter(Book.author_id == author_id).scalar()
        session.close()
        return count

    @classmethod
    def average_count_of_books(cls):
        start_range = datetime(year=datetime.today().year,
                              month=datetime.today().month,
                              day=1)
        end_range = datetime(year=datetime.today().year,
                              month=datetime.today().month + 1,
                              day=1)
        average_count = session.query(func.avg(Book.id)) \
            .join(ReceivingBook.book) \
            .filter(ReceivingBook.date_of_issue.between(start_range, end_range)) \
            .scalar()
        session.close()
        return average_count

    @classmethod
    def most_popular_book(cls):
        popular_book: Book = session.query(Book) \
            .join(ReceivingBook.book) \
            .join(ReceivingBook.student) \
            .filter(Student.average_score > 4) \
            .group_by(Book.id) \
            .order_by(func.count(Book.id).desc()) \
            .limit(1).one()

        session.close()
        return popular_book.to_json()


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
                                    lazy='select')
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

    @classmethod
    def top_students(cls):
        start_range = datetime(year=datetime.today().year,
                               month=1,
                               day=1)
        end_range = datetime(year=datetime.today().year + 1,
                             month=1,
                             day=1)
        top = session.query(Student) \
            .join(ReceivingBook.student) \
            .filter(ReceivingBook.date_of_issue.between(start_range, end_range)) \
            .group_by(ReceivingBook.student_id) \
            .order_by(func.count(ReceivingBook.student_id).desc()) \
            .limit(10).all()
        session.close()
        return [student.to_json() for student in top]

    @classmethod
    def bulk_insert(cls, new_students: csv.DictReader):
        new_students_list = [student for student in new_students]

        for student in new_students_list:
            if student['scholarship'] == '1':
                student['scholarship'] = True
            else:
                student['scholarship'] = False

        event.listen(Student, 'before_insert', on_student_insert)

        session.bulk_insert_mappings(Student, new_students_list)
        session.commit()

        all_students = session.query(Student).all()
        session.close()
        return [student.to_json() for student in all_students]


def on_student_insert(mapper, connection, target: Student):
    print(target.to_json())


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
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            return "Такая запись уже существует"

        result = session.query(ReceivingBook).filter(ReceivingBook.book_id == book_id,
                                                     ReceivingBook.student_id == student_id).one()
        session.close()
        return result

    @classmethod
    def receive_book(cls, book_id: int, student_id: int):
        book_for_receive: ReceivingBook = session.query(ReceivingBook).filter(
            ReceivingBook.book_id == book_id,
            ReceivingBook.student_id == student_id
        ).one_or_none()
        if book_for_receive:
            book_for_receive.date_of_return = datetime.now()
            session.commit()

            updated_line = session.query(ReceivingBook).filter(ReceivingBook.book_id == book_id,
                                                               ReceivingBook.student_id == student_id).one()
            session.close()
            return updated_line

        session.close()
        return f'Ошибка: записи с book_id = {book_id} и student_id = {student_id} не существует!'

    @classmethod
    def unread_books_by_student(cls, student_id: int):
        books_id_q = session.query(Book.id) \
            .join(ReceivingBook.book) \
            .filter(ReceivingBook.student_id == student_id).subquery()

        authors_id_q = session.query(Book.author_id).distinct(Book.author_id) \
            .join(ReceivingBook.book) \
            .filter(ReceivingBook.student_id == student_id).subquery()

        unread_books = session.query(Book) \
            .filter(Book.author_id.in_(authors_id_q),
                    Book.id.notin_(books_id_q)).all()

        session.close()
        return [book.to_json() for book in unread_books]



