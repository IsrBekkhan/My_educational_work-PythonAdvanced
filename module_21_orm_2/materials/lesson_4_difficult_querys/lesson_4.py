from sqlalchemy import Column, Integer, Float, String, Boolean, Date, \
    ForeignKey, DateTime, create_engine, func, desc
from sqlalchemy.orm import relationship, sessionmaker, backref, joinedload
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime, date

engine = create_engine('sqlite:///lesson3.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Author(Base):
    # таблица авторов
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(100), nullable=False)

    def __repr__(self):
        return self.name + ' ' + self.surname


class Book(Base):
    # таблица книг
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)

    author = relationship("Author", backref=backref("books",
                                                    cascade="all, "
                                                            "delete-orphan",
                                                    lazy="select"))

    students = relationship('ReceivingBook', back_populates='book')


class Student(Base):
    # таблица читателей-студентов
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(100), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    books = relationship('ReceivingBook', back_populates='student')


class ReceivingBook(Base):
    # таблица выдачи книг студентам
    __tablename__ = 'receiving_books'

    book_id = Column(Integer, ForeignKey('books.id'),
                     primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'),
                        primary_key=True)

    date_of_issue = Column(DateTime, default=datetime.now)
    date_of_finish = Column(DateTime, nullable=True)

    student = relationship("Student", back_populates="books")
    book = relationship("Book", back_populates="students")


def insert_data():
    authors = [Author(name="Александр", surname="Пушкин"),
               Author(name="Лев", surname="Толстой"),
               Author(name="Михаил", surname="Булгаков"),
               ]
    authors[0].books.extend([Book(name="Капитанская дочка",
                                  count=5,
                                  release_date=date(1836, 1, 1)),
                             Book(name="Евгений Онегин",
                                  count=3,
                                  release_date=date(1838, 1, 1))
                             ])
    authors[1].books.extend([Book(name="Война и мир",
                                  count=10,
                                  release_date=date(1867, 1, 1)),
                             Book(name="Анна Каренина",
                                  count=7,
                                  release_date=date(1877, 1, 1))
                             ])
    authors[2].books.extend([Book(name="Морфий",
                                  count=5,
                                  release_date=date(1926, 1, 1)),
                             Book(name="Собачье сердце",
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