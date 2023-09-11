from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError

from models import (
    BOOKS_DATA,
    AUTHORS_DATA,
    Book,
    Author,
    get_all_books,
    get_book_by_id,
    update_book_by_id,
    update_book_patch_by_id,
    delete_book_by_id,
    get_all_authors,
    get_all_books_by_author,
    delete_author_by_id,
    add_author,
    add_author_and_book,
    init_db,
    add_book,
)
from schemas import BookSchema, BookSchemaPatch, AuthorSchema

app = Flask(__name__)
api = Api(app)


class BookList(Resource):

    @staticmethod
    def get(book_id: int = None) -> tuple[dict, int]:
        schema = BookSchema()
        if book_id is not None:
            return schema.dump(get_book_by_id(book_id)), 200
        return {"data": schema.dump(get_all_books(), many=True)}, 200

    @staticmethod
    def post() -> tuple[dict, int]:
        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        book = add_book(book)
        return schema.dump(book), 201

    @staticmethod
    def put(book_id: int) -> tuple[dict, int]:
        data = request.json
        schema = BookSchema()
        try:
            book: Book = schema.load(data)
            book.id = book_id
        except ValidationError as exc:
            return exc.messages, 400

        update_book_by_id(book)
        return schema.dump(get_book_by_id(book_id)), 201

    @staticmethod
    def patch(book_id: int) -> tuple[dict, int]:
        data = request.json
        schema = BookSchemaPatch()
        try:
            book_data = schema.load(data, partial=True)
        except ValidationError as exc:
            return exc.messages, 400

        update_book_patch_by_id(book_id, book_data)
        return schema.dump(get_book_by_id(book_id)), 201

    @staticmethod
    def delete(book_id: int) -> tuple[dict, int]:
        schema = BookSchema()
        delete_book_by_id(book_id)
        return {"data": schema.dump(get_all_books(), many=True)}, 200


class AuthorList(Resource):

    @staticmethod
    def get(author_id: int = None):
        author_schema = AuthorSchema()
        book_schema = BookSchema()

        if author_id is not None:
            return {"data": book_schema.dump(get_all_books_by_author(author_id), many=True)}, 200
        return {"data": author_schema.dump(get_all_authors(), many=True)}, 200

    @staticmethod
    def post():
        data = request.json
        schema = AuthorSchema()
        try:
            author: Author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        if author.title is not None:
            return schema.dump(add_author_and_book(author)), 201

        author = add_author(author)
        return schema.dump(author), 201


    @staticmethod
    def delete(author_id: int):
        return delete_author_by_id(author_id)


api.add_resource(BookList, '/api/books', '/api/books/<int:book_id>')
api.add_resource(AuthorList, '/api/authors', '/api/authors/<int:author_id>')


if __name__ == '__main__':
    init_db(book_records=BOOKS_DATA, author_records=AUTHORS_DATA)
    app.run(debug=True)
