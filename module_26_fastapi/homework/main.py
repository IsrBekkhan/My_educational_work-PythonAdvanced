from fastapi import FastAPI, Path
from sqlalchemy.future import select

from typing import List, Any

from database import engine, session
import models
from schemas import RecipeDetails, RecipeViews


app = FastAPI()


@app.on_event('startup')
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    await session.commit()


@app.on_event('shutdown')
async def shutdown_event():
    await session.close()
    await engine.dispose()


@app.post('/recipes', response_model=RecipeDetails)
async def post_recipe(recipe: RecipeDetails) -> models.Recipe:
    new_recipe = models.Recipe(
        name=recipe.name,
        cooking_time=recipe.cooking_time,
        description=recipe.description,
        ingredients=[
            models.Ingredient(**ingredient.dict()) for ingredient in recipe.ingredients
        ]
    )
    async with session.begin():
        await session.merge(new_recipe)
    await session.commit()

    return new_recipe


@app.get('/recipes', response_model=List[RecipeViews])
async def get_recipes() -> List[models.Recipe]:
    res = await session.execute(
        select(
            models.Recipe.name,
            models.Recipe.cooking_time,
            models.Recipe.views_count
        )
    )
    recipes_list = res.unique().scalars().all()

    for recipe in recipes_list:
        print(dir(recipe))

    return recipes_list


@app.get('/recipes/{name}', response_model=RecipeDetails)
async def get_recipe(recipe_name: str) -> models.Recipe:
    res = await session.execute(
        select(models.Recipe).where(models.Recipe.name.like(recipe_name))
    )
    recipe = res.scalars().first()

    print(RecipeDetails.from_orm(recipe))

    return recipe

