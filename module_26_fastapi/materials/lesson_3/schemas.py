from pydantic import BaseModel


class BaseBook(BaseModel):
    title: str
    author: str

class BookIn(BaseBook):
    ...

class BookOut(BaseBook):
    id: int

    class Config:
        orm_mode = True
