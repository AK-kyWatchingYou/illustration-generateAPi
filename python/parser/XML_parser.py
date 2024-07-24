import xml.etree.ElementTree as ET
import json
from pydantic import BaseModel
from typing import List

class Ingredient(BaseModel):
    ingredient_name: str
    ingredient_amount: str

class Recipe(BaseModel):
    recipe_name: str
    recipe_description: str
    ingredients: List[Ingredient]
    instructions: List[str]

class RecipeBook(BaseModel):
    brainstorming: str
    recipes: List[Recipe]

def parse_recipi(xml_data):
    # create ElementTree object
    root = ET.fromstring(xml_data)

    # parse brainstorming element
    brainstorming = root.find('brainstorming').text.strip()

    # parse recipe elements
    recipes = []
    for recipe_elem in root.findall('recipe'):
        recipe_name = recipe_elem.find('recipe_name').text
        recipe_description = recipe_elem.find('recipe_description').text

        ingredients = []
        for ingredient_elem in recipe_elem.find('ingredients').findall('ingredient'):
            ingredient_name = ingredient_elem.find('ingredient_name').text
            ingredient_amount = ingredient_elem.find('ingredient_amount').text
            ingredients.append(
                Ingredient(
                    ingredient_name=ingredient_name,
                    ingredient_amount=ingredient_amount
                )
            )

        instructions = recipe_elem.find('instructions').text.strip().split('\n')

        recipes.append(
            Recipe(
                recipe_name=recipe_name,
                recipe_description=recipe_description,
                ingredients=ingredients,
                instructions=instructions
            )
        )

    # create RecipeBook
    recipe_book = RecipeBook(
        brainstorming=brainstorming,
        recipes=recipes
    )

    # convert to JSON format
    # json_result = json.dumps(recipe_book, ensure_ascii=False, indent=2, default=lambda o: o.__dict__)

    return recipe_book.dict()
