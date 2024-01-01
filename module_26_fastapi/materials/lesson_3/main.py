from typing import List

from fastapi import FastAPI
from sqlalchemy.future import select

import models
import schemas
from database import engine, session

app = FastAPI()


@app.on_event("startup")
async def shutdown():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.post('/books/', response_model=schemas.BookOut)
async def books(book: schemas.BookIn) -> models.Book:
    new_book = models.Book(**book.dict())
    async with session.begin():
        session.add(new_book)
    return new_book


@app.get('/books/', response_model=List[schemas.BookOut])
async def books() -> List[models.Book]:
    res = await session.execute(select(models.Book))
    return res.scalars().all()
