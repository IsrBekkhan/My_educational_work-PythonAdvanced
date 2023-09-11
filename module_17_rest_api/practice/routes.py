from dataclasses import asdict

from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError

from models import DATA, get_all_books, init_db, add_book, Book, get_book_by_title, get_books_by_author
from schemas import BookSchema


app = Flask(__name__)
api = Api(app)


class BookList(Resource):

    @staticmethod
    def get(author: str = None):
        schema = BookSchema()
        if author:
            return {"data": schema.dump(get_books_by_author(author), many=True)}, 200
        return {"data": schema.dump(get_all_books(), many=True)}, 200

    @staticmethod
    def post():

        data = request.json
        schema = BookSchema()

        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        book = add_book(book)
        return schema.dump(book), 201


api.add_resource(BookList, '/api/books', '/api/books/<author>')


if __name__ == '__main__':
    init_db(initial_records=DATA)
    app.run(debug=True)