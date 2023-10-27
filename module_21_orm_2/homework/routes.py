from flask import Flask, jsonify, request
from validators import BookForm
from csv import DictReader

from models import Base, engine, Book, ReceivingBook, Student

app = Flask(__name__)


@app.before_request
def before_request_func():
    Base.metadata.create_all(bind=engine)


# Решение задания 2.1
@app.route('/books/<int:author_id>', methods=['GET'])
def get_books_count_by_author_id(author_id: int):
    """
    Получить кол-во оставшихся в библиотеке книг по ID автора
    """
    return jsonify(books_count_by_author=Book.get_books_count_by_author_id(author_id)), 200


# Решение задания 2.2
@app.route('/unread_books/<int:student_id>', methods=['GET'])
def unread_books_by_student(student_id: int):
    """
    Получить список книг, которые студент не читал,
    при этом другие книги этого автора студент уже брал
    """
    return jsonify(unread_books=ReceivingBook.unread_books_by_student(student_id))


# Решение задания 2.3
@app.route('/avg_books', methods=['GET'])
def average_of_books():
    """
    Получить среднее кол-во книг, которые студенты брали в этом месяце
    """
    return jsonify(average_count_of_books=Book.average_count_of_books()), 200


# Решение задания 2.4
@app.route('/popular_book', methods=['GET'])
def most_popular_book():
    """
    Получить самую популярную книгу среди студентов,
    у которых средний балл больше 4.0
    """
    return jsonify(most_popular_book=Book.most_popular_book())


# Решение задания 2.5
@app.route('/top_students', methods=['GET'])
def top_students():
    """
    Получить ТОП-10 самых читающих студентов в этом году
    """
    return jsonify(top_students=Student.top_students())


# Решение задания #3
@app.route('/bulk', methods=['POST'])
def bulk_insert():
    """
    Принять csv-файл с данными по студентам для массовой вставки
    POST
    form-data:
        file: <file_path>
    """
    if request.files:
        csv_file = request.files.get('file')
        csv_file.save(csv_file.filename)

        with open(csv_file.filename) as file_:
            new_students = DictReader(file_, delimiter=';')
            return jsonify(new_students_list=Student.bulk_insert(new_students)), 201

    return "Отсутствует csv-файл!", 404


# Задание предыдущего модуля!
@app.route('/books', methods=['GET'])
def get_all_books():
    """ Получить все книги """
    return jsonify(all_books=Book.all_books()), 200


# Задание предыдущего модуля!
@app.route('/books/<title>', methods=['GET'])
def get_book_by_title(title: str):
    """ Получить книгу по названию """
    result = Book.get_book_by_title(title)
    if result:
        return jsonify(the_book=Book.get_book_by_title(title).to_json()), 200
    return f'Книга с названием {title} не найдена в БД!', 400


# Задание предыдущего модуля!
@app.route('/debtors', methods=['GET'])
def get_all_debtors():
    """
    Получить список должников, которые держат книги у себя более 14 дней.
    """
    return jsonify(all_debtors=ReceivingBook.all_debtors()), 200


# Задание предыдущего модуля!
@app.route('/gives', methods=['POST'])
def giving_books():
    """
    Выдать книгу студенту
    POST
    form-data:
        student_id: int
        book_id: int
    """
    form = BookForm()

    if form.validate_on_submit():
        book_id, student_id = form.book_id.data, form.student_id.data
        new_line = ReceivingBook.add_line(book_id, student_id)
        if isinstance(new_line, str):
            return 'Такая запись уже существует!', 403
        return jsonify(new_line=new_line.to_json()), 201

    return jsonify(input_errors=form.errors), 400


# Задание предыдущего модуля!
@app.route('/receives', methods=['POST'])
def receiving_books():
    """
    Cдать книгу в библиотеку
    POST
    form-data:
        student_id: int
        book_id: int
    """
    form = BookForm()

    if form.validate_on_submit():
        book_id, student_id = form.book_id.data, form.student_id.data
        result = ReceivingBook.receive_book(book_id, student_id)

        if isinstance(result, str):
            return result, 400
        return jsonify(all_lines=result.to_json()), 201

    return jsonify(input_errors=form.errors), 400


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)