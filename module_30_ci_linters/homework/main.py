from typing import List

from fastapi import FastAPI, status
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

import models
from database import Base, async_engine, session
from schemas import RecipeDetails, RecipeViews

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await session.commit()


@app.on_event("shutdown")
async def shutdown_event():
    await session.close()
    await async_engine.dispose()


@app.post("/recipes", response_model=RecipeDetails, status_code=status.HTTP_201_CREATED)
async def post_recipe(recipe: RecipeDetails) -> models.Recipe:
    new_recipe = models.Recipe(
        name=recipe.name.lower(),
        cooking_time=recipe.cooking_time,
        description=recipe.description,
        ingredients=[
            models.Ingredient(**ingredient.dict()) for ingredient in recipe.ingredients
        ],
    )
    async with session.begin():
        await session.merge(new_recipe)
    await session.commit()
    await session.close()

    return new_recipe


@app.get("/recipes", response_model=List[RecipeViews])
async def get_recipes() -> List[models.Recipe]:
    res = await session.execute(select(models.Recipe))
    recipe = res.unique().scalars().all()
    await session.close()

    return recipe


@app.get("/recipes/{recipe_name}", response_model=RecipeDetails)
async def get_recipe(recipe_name: str) -> models.Recipe:

    res = await session.execute(
        select(models.Recipe)
        .options(selectinload(models.Recipe.ingredients))
        .where(models.Recipe.name == recipe_name.lower())
    )

    recipe: models.Recipe = res.scalars().first()

    recipe.views_count += 1
    await session.close()

    async with session.begin():
        await session.merge(recipe)
    await session.commit()
    await session.close()

    return recipe
