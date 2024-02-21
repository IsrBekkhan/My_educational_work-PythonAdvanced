from typing import List

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

integration_table = Table(
    "integrations",
    Base.metadata,
    Column("recipe_name", ForeignKey("recipes.name"), primary_key=True),
    Column("ingredient_name", ForeignKey("ingredients.name"), primary_key=True),
)


class Ingredient(Base):
    __tablename__ = "ingredients"

    name: Mapped[str] = mapped_column(String(50), primary_key=True)


class Recipe(Base):
    __tablename__ = "recipes"

    name: Mapped[str] = mapped_column(String(50), primary_key=True)
    cooking_time: Mapped[int]
    description: Mapped[str] = mapped_column(String(300), default="")
    views_count: Mapped[int] = mapped_column(default=0)

    ingredients: Mapped[List[Ingredient]] = relationship(
        secondary=integration_table, cascade="all"
    )
