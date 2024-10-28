from typing import List, Dict, Callable
from functools import reduce

def filter_recipes_by_ingredient(recipes: List[Dict[str, str]], ingredient: str) -> List[Dict[str, str]]:
    return list(filter(lambda recipe: ingredient in recipe['ingredients'], recipes))

def get_recipe_titles(recipes: List[Dict[str, str]]) -> List[str]:
    return list(map(lambda recipe: recipe['title'], recipes))

def count_total_ingredients(recipes: List[Dict[str, str]]) -> int:
    return reduce(lambda acc, recipe: acc + len(recipe['ingredients'].split(', ')), recipes, 0)

def create_recipe(title: str) -> Callable[[List[str], List[str]], None]:
    def recipe(ingredients: List[str], steps: List[str]):
        from models import Recipe
        new_recipe = Recipe(title, ingredients, steps)
        new_recipe.save()
    return recipe
