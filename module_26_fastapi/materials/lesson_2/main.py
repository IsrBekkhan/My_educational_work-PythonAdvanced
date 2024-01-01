from typing import Dict, Optional

from fastapi import FastAPI, Path, Query, Body
from pydantic import Field, BaseModel

app = FastAPI()


@app.get("/async")
async def hello_async() -> Dict[str, str]:
    return {"message": "Hello World"}


@app.get("/sync")
def hello_async() -> Dict[str, str]:
    return {"message": "Hello World"}


@app.get('/hello/{who}')
async def say_hello(
    who: int = Path(
        ...,
        title='Id of the user to whom to send the message.',
        ge=0,
        le=4,
    ),
    message: Optional[str] = Query(
        None,
        title="Say something pleasant to the user. Don't be arrogant (do not use uppercase)",
        regex='^[a-z0-9_\-]+$'
    )
):
    fake_users_db = {1: 'admin', 2: 'John'}
    user = fake_users_db.get(who, 'username')
    return {'message': f'{message}, {user}'}



class Author(BaseModel):
    name: str
    born_year: int = Field(..., lt=2015)


class Book(BaseModel):
    title: str = Field(
        ...,
        title='Full title of the book.',
        min_length=3,
        max_length=100
    )
    author: Author
    text: Optional[str] = None


@app.post('/books')
@app.post('/books/{idx}')
async def post_book(
    book: Book,
    publisher: Optional[str] = Body(...),
    idx: Optional[int] = None
):
    publisher_message = f'It was published by {publisher}' if publisher else ''
    return {
        'message': f"{book.author.name} wrote a great book!"
                   + publisher_message
                   + f" I definitely will read {book.title}!"
    }
