from fastapi.testclient import TestClient

from main import app
from schemas import RecipeDetails, Ingredient


client = TestClient(app)


def test_get_recipes():
    response = client.get('/recipes')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_recipe():
    recipe_name = 'get_test'.lower()
    recipe = RecipeDetails(
        name=recipe_name,
        cooking_time=35,
        description="get_test description",
        ingredients=[
            Ingredient(name="get_test ingredient_1"),
            Ingredient(name="get_test ingredient_2")
        ]
    )
    post_response = client.post('/recipes', json=recipe.dict())
    get_response = client.get(f'/recipes/{recipe_name}')

    assert get_response.status_code == 200
    assert get_response.json() == recipe.dict()


def test_post_recipe():
    recipe_name = 'post_test'.lower()
    recipe = RecipeDetails(
        name=recipe_name,
        cooking_time=35,
        description="post_test description",
        ingredients=[
            Ingredient(name="post_test_ingredient_1"),
            Ingredient(name="post_test_ingredient_2")
        ]
    )
    response = client.post('/recipes', json=recipe.dict())
    assert response.status_code == 201
    assert response.json() == recipe.dict()
