from pydantic import BaseModel, Field
from typing import List, Optional


class Ingredient(BaseModel):
    name: str = Field(
        ...,
        title="Название ингридиента",
        min_length=1,
        max_length=50
    )

    class Config:
        orm_mode = True


class Recipe(BaseModel):
    name: str = Field(
        ...,
        title='Название кулинарного рецепта',
        min_length=1,
        max_length=50
    )
    cooking_time: int = Field(
        ...,
        title='Время готовки рецепта в минутах',
        ge=1,
        le=60
    )


class RecipeViews(Recipe):
    views_count: Optional[int] = Field(0, title='Количество просмотров рецепта')

    class Config:
        orm_mode = True


class RecipeDetails(Recipe):
    ingredients: List[Ingredient] = Field(
        ...,
        title='Список ингридиентов рецепта'
    )
    description: Optional[str] = Field(
        '',
        title='Описание рецепта',
        max_length=300
    )

    class Config:
        orm_mode = True
