from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError

from werkzeug.serving import WSGIRequestHandler

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

# imports for documentation
from flasgger import APISpec, Swagger, swag_from
from swag_from_json import swag_from_json
from apispec_webframeworks.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin

app = Flask(__name__)
api = Api(app)

# spec = APISpec(
#     title='BooksAndAuthors',
#     version='1.0.0',
#     openapi_version='2.0',
#     plugins=[
#         FlaskPlugin(),
#         MarshmallowPlugin()
#     ]
# )


class BookList(Resource):

    @staticmethod
    @swag_from('../books_documentation/books-get.yml')
    def get(book_id: int = None) -> tuple[dict, int]:
        schema = BookSchema()
        if book_id is not None:
            return schema.dump(get_book_by_id(book_id)), 206
        return schema.dump(get_all_books(), many=True), 200

    @staticmethod
    @swag_from('../books_documentation/books-post.yml')
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
    @swag_from('../books_documentation/books-put.yml')
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
    @swag_from('../books_documentation/books-patch.yml')
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
    @swag_from('../books_documentation/books-delete.yml')
    def delete(book_id: int) -> tuple[dict, int]:
        schema = BookSchema()
        delete_book_by_id(book_id)
        return schema.dump(get_all_books(), many=True), 200


class AuthorList(Resource):

    @staticmethod
    @swag_from_json('../authors_documentation/authors_get.json')
    def get(author_id: int = None):
        author_schema = AuthorSchema()
        book_schema = BookSchema()

        if author_id is not None:
            return {"data": book_schema.dump(get_all_books_by_author(author_id), many=True)}, 200
        return {"data": author_schema.dump(get_all_authors(), many=True)}, 206

    @staticmethod
    @swag_from_json('../authors_documentation/authors_post.json')
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
    @swag_from_json('../authors_documentation/authors_delete.json')
    def delete(author_id: int):
        return delete_author_by_id(author_id)


# template = spec.to_flasgger(
#     app,
#     definitions=[BookSchema, AuthorSchema]
# )

swagger = Swagger(app)

api.add_resource(BookList, '/api/books', '/api/books/<int:book_id>')
api.add_resource(AuthorList, '/api/authors', '/api/authors/<int:author_id>')


if __name__ == '__main__':
    init_db(book_records=BOOKS_DATA, author_records=AUTHORS_DATA)
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(debug=True)
