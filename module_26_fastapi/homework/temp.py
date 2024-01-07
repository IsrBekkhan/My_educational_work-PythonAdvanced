from schemas import RecipeDetails, RecipeViews
from models import Recipe, Ingredient
from database import Base, session, engine
import asyncio
from sqlalchemy.ext.asyncio import AsyncResult

from sqlalchemy.future import select

model_dict = {
    "name": "Другой шашлык 2",
    "cooking_time": 15,
    "ingredients": ['перец', 'баранина', 'мускус'],
    "description": "Мощный сочный шашлык"
}


async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await session.commit()


async def db_add():
    ingredients = [Ingredient(name=name) for name in model_dict['ingredients']]
    new_recipe = Recipe(name=model_dict['name'],
                        cooking_time=model_dict['cooking_time'],
                        description=model_dict['description'],
                        ingredients=ingredients)
    async with session.begin():
        await session.merge(new_recipe)
    await session.commit()


async def db_get():
    res = await session.execute(
        select(Recipe).where(Recipe.name.like('Шашлык'))
    )
    model = res.scalars().first()
    print(RecipeViews.from_orm(model))


async def shutdown():
    await session.close()
    await engine.dispose()


async def main():
    await startup()
    await db_get()
    await shutdown()


asyncio.run(main())
