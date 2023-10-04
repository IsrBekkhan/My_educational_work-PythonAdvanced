from flasgger import Schema, fields, ValidationError
from marshmallow import validates, post_load

from models import get_book_by_title, get_author_by_id, Book, Author, is_author_exists
from typing import Optional


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author_id = fields.Int(required=True)

    @validates('title')
    def validate_title(self, title: str) -> None:
        if get_book_by_title(title) is not None:
            raise ValidationError(
                "Book with title '{title}' already exists, "
                "please use a different title.".format(title=title)
            )

    @validates('author_id')
    def validate_author(self, author_id: int) -> None:
        if get_author_by_id(author_id) is None:
            raise ValidationError(
                'Автора с id-{id} нет в базе данных'.format(id=author_id)
            )


    @post_load
    def create_book(self, data: dict, **kwargs) -> Book:
        return Book(**data)


class BookSchemaPatch(BookSchema):

    @post_load
    def create_book(self, data: dict, **kwargs) -> dict:
        return data


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    middle_name = fields.Str(default=None)
    title = fields.Str(default=None)

    @post_load
    def create_author(self, data: dict, **kwargs) -> Optional[Author]:
        author = Author(**data)
        if author.middle_name is not None:
            error_message = f'{author.first_name} {author.middle_name} {author.last_name} уже есть в базе данных'
        else:
            error_message = f'{author.first_name} {author.last_name} уже есть в базе данных'
        if is_author_exists(author):
            raise ValidationError(error_message)
        return author

