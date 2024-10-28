from typing import List, Dict
from functools import reduce

def filter_recipes_by_ingredient(recipes: List[Dict[str, str]], ingredient: str) -> List[Dict[str, str]]:
    return list(filter(lambda recipe: ingredient in recipe['ingredients'], recipes))

def get_recipe_titles(recipes: List[Dict[str, str]]) -> List[str]:
    return list(map(lambda recipe: recipe['title'], recipes))

def count_total_ingredients(recipes: List[Dict[str, str]]) -> int:
    return reduce(lambda acc, recipe: acc + len(recipe['ingredients'].split(', ')), recipes, 0)
