from flask import Flask, jsonify
from validators import BookForm
from models import Base, engine, Book, ReceivingBook

app = Flask(__name__)


@app.before_request
def before_request_func():
    Base.metadata.create_all(engine)


@app.route('/books', methods=['GET'])
def get_all_books():
    return jsonify(all_books=Book.all_books()), 200


@app.route('/books/<title>', methods=['GET'])
def get_book_by_title(title: str):
    result = Book.get_book_by_title(title)
    if result:
        return jsonify(the_book=Book.get_book_by_title(title).to_json()), 200
    return f'Книга с названием {title} не найдена в БД!', 400


@app.route('/debtors', methods=['GET'])
def get_all_debtors():
    return jsonify(all_debtors=ReceivingBook.all_debtors()), 200


@app.route('/gives', methods=['POST'])
def giving_books():
    form = BookForm()

    if form.validate_on_submit():
        book_id, student_id = form.book_id.data, form.student_id.data
        new_line = ReceivingBook.add_line(book_id, student_id)
        return jsonify(new_line=new_line.to_json()), 201

    return jsonify(input_errors=form.errors), 400


@app.route('/receives', methods=['POST'])
def receiving_books():
    form = BookForm()

    if form.validate_on_submit():
        book_id, student_id = form.book_id.data, form.student_id.data
        result = ReceivingBook.delete_line(book_id, student_id)

        if isinstance(result, str):
            return result, 400
        return jsonify(all_lines=result)

    return jsonify(input_errors=form.errors), 400


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)