from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

from database import Base


integration_table = Table('integrations', Base.metadata,
                          Column('recipe_name',
                                 ForeignKey('recipes.name'),
                                 primary_key=True),
                          Column('ingredient_name',
                                 ForeignKey('ingredients.name'),
                                 primary_key=True)
                          )


class Ingredient(Base):
    __tablename__ = 'ingredients'

    name = Column(String(50), primary_key=True, nullable=False)


class Recipe(Base):
    __tablename__ = 'recipes'

    name = Column(
        String(50),
        primary_key=True,
        nullable=False
    )
    cooking_time = Column(Integer, nullable=False)
    description = Column(String(300), default='', nullable=True)
    views_count = Column(Integer, default=0, nullable=False)

    ingredients = relationship('Ingredient',
                               secondary=integration_table,
                               cascade='all',
                               lazy='joined')




