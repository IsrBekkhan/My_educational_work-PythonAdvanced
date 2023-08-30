from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

from typing import List, Union, Tuple

from models import init_db, get_all_books, DATA, add_new_book, get_authors_books, get_book_info

app: Flask = Flask(__name__)


class BookAddForm(FlaskForm):
    required_error_message = 'Это поле обязательно к заполнению'

    book_title = StringField(validators=[
        InputRequired(message=required_error_message)
    ])
    author_name = StringField(validators=[
        InputRequired(message=required_error_message)
    ])


def _get_html_table_for_books(books: List[dict]) -> str:
    table = """
<table>
    <thead>
    <tr>
        <th>ID</td>
        <th>Title</td>
        <th>Author</td>
    </tr>
    </thead>
    <tbody>
        {books_rows}
    </tbody>
</table>
"""
    rows: str = ''
    for book in books:
        rows += '<tr><td>{id}</tb><td>{title}</tb><td>{author}</tb></tr>'.format(
            id=book['id'], title=book['title'], author=book['author'],
        )
    return table.format(books_rows=rows)


@app.route('/books')
def all_books() -> str:
    return render_template(
        'index.html',
        books=get_all_books(),
    )


@app.route('/books/form', methods=['GET', 'POST'])
def get_books_form() -> Union[str, Tuple[str, int]]:
    if request.method == 'POST':
        validate_form = BookAddForm()

        if validate_form.validate_on_submit():
            book_title = validate_form.book_title.data
            author_name = validate_form.author_name.data
            add_new_book(book_title, author_name)
            return all_books()

        return f"Invalid input, {validate_form.errors}", 400

    return render_template('add_book.html')


@app.route('/search/<author>')
def search(author: str):
    authors_books = get_authors_books(author)

    return render_template(
        'index.html',
        authors_books=authors_books
    )


@app.route('/books/<int:book_id>')
def book_info_from_id(book_id: int):
    return render_template(
        'index.html',
        book_info=get_book_info(book_id)
    )


if __name__ == '__main__':
    init_db(DATA)
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
