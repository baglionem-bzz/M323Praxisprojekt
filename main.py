from database import init_db, get_recipes
from functional_utils import create_recipe, filter_recipes_by_ingredient, get_recipe_titles, count_total_ingredients


def main():
    init_db()

    new_recipe = create_recipe("Schokoladenkuchen")
    new_recipe(["Mehl", "Zucker", "Kakao", "Butter", "Eier"], ["Mischen", "Backen"])

    recipes = get_recipes()
    print("Alle Rezepte:", recipes)

    chocolate_recipes = filter_recipes_by_ingredient(recipes, "Kakao")
    print("Rezepte mit Kakao:", get_recipe_titles(chocolate_recipes))

    total_ingredients = count_total_ingredients(recipes)
    print("Gesamtanzahl der Zutaten in allen Rezepten:", total_ingredients)


if __name__ == '__main__':
    main()
