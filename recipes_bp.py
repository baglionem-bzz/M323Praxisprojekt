from flask import Blueprint, request, jsonify
from recipe import Recipe
from recipe_dao import RecipeDao
from functools import reduce

# Blueprint erstellen
recipes_bp = Blueprint('recipes', __name__)

# Instanz des RecipeDao für Datenbankoperationen
recipe_dao = RecipeDao('recipe_collector.db')


@recipes_bp.route('/', methods=['GET'])
def get_all_recipes():
    recipes = recipe_dao.get_all_recipes()
    return jsonify([recipe.__dict__ for recipe in recipes]), 200


@recipes_bp.route('/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = recipe_dao.get_recipe(recipe_id)
    if recipe:
        return jsonify(recipe.__dict__), 200
    else:
        return jsonify({'message': 'Recipe not found'}), 404


@recipes_bp.route('/', methods=['POST'])
def add_recipe():
    data = request.get_json()
    new_recipe = Recipe(1, data['title'], data['ingredients'], data['steps'])
    recipe_dao.add_recipe(new_recipe)
    return jsonify({'message': 'Recipe created'}), 201


@recipes_bp.route('/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    data = request.get_json()
    updated_recipe = Recipe(recipe_id, data['title'], data['ingredients'], data['steps'])
    if recipe_dao.update_recipe(updated_recipe):
        return jsonify({'message': 'Recipe updated'}), 200
    else:
        return jsonify({'message': 'Recipe not found or not updated'}), 404


@recipes_bp.route('/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    if recipe_dao.delete_recipe(recipe_id):
        return jsonify({'message': 'Recipe deleted'}), 200
    else:
        return jsonify({'message': 'Recipe not found or not deleted'}), 404


@recipes_bp.route('/<int:recipe_id>', methods=['GET', 'DELETE'])
def handle_recipe(recipe_id):
    if request.method == 'GET':
        return get_recipe_response(recipe_id)
    elif request.method == 'DELETE':
        return delete_recipe_response(recipe_id)


def get_recipe_response(recipe_id):
    recipe = recipe_dao.get_recipe(recipe_id)
    return jsonify(recipe.__dict__) if recipe else jsonify({'message': 'Recipe not found'}), 404

def delete_recipe_response(recipe_id):
    success = recipe_dao.delete_recipe(recipe_id)
    return jsonify({'message': 'Recipe deleted'}) if success else jsonify({'message': 'Recipe not found'}), 404



def recipe_operation_context(recipe_id=None):
    """
    Ein Closure, das je nach Vorhandensein einer ID die entsprechende Funktion zurückgibt.
    """
    def add_or_update_recipe(recipe):
        if recipe_id:
            return recipe_dao.update_recipe(recipe)
        else:
            return recipe_dao.add_recipe(recipe)
    return add_or_update_recipe

@recipes_bp.route('/recipe', methods=['POST'])
def upsert_recipe():
    """
    Fügt ein Rezept hinzu oder aktualisiert es, abhängig davon, ob eine ID vorhanden ist.
    """
    data = request.get_json()
    recipe_id = data.get('id')
    operation = recipe_operation_context(recipe_id)
    recipe = Recipe(recipe_id, data['title'], data['ingredients'], data['steps'])
    success = operation(recipe)
    message = 'Recipe updated' if recipe_id else 'Recipe created'
    return jsonify({'message': message, 'success': success}), 200

@recipes_bp.route('/uppercase_title/<int:recipe_id>', methods=['GET'])
def get_recipe_with_uppercase_title(recipe_id):
    """
    Holt ein Rezept und gibt den Titel in Großbuchstaben zurück.
    """
    recipe = recipe_dao.get_recipe(recipe_id)
    to_upper = lambda s: s.upper()  # Lambda-Ausdruck für Großbuchstaben
    if recipe:
        recipe.title = to_upper(recipe.title)
        return jsonify(recipe.__dict__), 200
    else:
        return jsonify({'message': 'Recipe not found'}), 404

@recipes_bp.route('/summary/<int:recipe_id>', methods=['GET'])
def get_recipe_summary(recipe_id):
    """
    Holt eine Zusammenfassung des Rezepts mit Titel, Zutaten und Schritten.
    """
    recipe = recipe_dao.get_recipe(recipe_id)
    format_summary = lambda title, ingredients, steps: f"{title}: {ingredients} - {steps}"
    if recipe:
        summary = format_summary(recipe.title, recipe.ingredients, recipe.steps)
        return jsonify({'summary': summary}), 200
    else:
        return jsonify({'message': 'Recipe not found'}), 404

@recipes_bp.route('/sorted_recipes', methods=['GET'])
def get_sorted_recipes():
    """
    Gibt alle Rezepte alphabetisch sortiert nach Titel zurück.
    """
    recipes = recipe_dao.get_all_recipes()
    sorted_recipes = sorted(recipes, key=lambda recipe: recipe.title)
    return jsonify([recipe.__dict__ for recipe in sorted_recipes]), 200

@recipes_bp.route('/processed_recipes', methods=['GET'])
def get_processed_recipes():
    recipes = recipe_dao.get_all_recipes()

    titles_uppercase = list(map(lambda recipe: recipe.title.upper(), recipes))

    sugar_recipes = list(filter(lambda recipe: "Zucker" in recipe.ingredients, recipes))

    total_steps = reduce(lambda acc, recipe: acc + len(recipe.steps.split()), recipes, 0)

    return jsonify({
        'titles_uppercase': titles_uppercase,
        'sugar_recipes': [recipe.__dict__ for recipe in sugar_recipes],
        'total_steps': total_steps
    }), 200

@recipes_bp.route('/complex_process', methods=['GET'])
def get_complex_process():
    """
    Filtert Rezepte nach einer Zutat, konvertiert Titel in Großbuchstaben und berechnet die Gesamtanzahl der Wörter in den Schritten.
    """
    recipes = recipe_dao.get_all_recipes()

    filtered_recipes = list(filter(lambda recipe: "Zucker" in recipe.ingredients, recipes))

    titles_uppercase = list(map(lambda recipe: recipe.title.upper(), filtered_recipes))

    total_words = reduce(lambda acc, recipe: acc + len(recipe.steps.split()), filtered_recipes, 0)

    return jsonify({
        'titles_uppercase': titles_uppercase,
        'total_words_in_steps': total_words
    }), 200

@recipes_bp.route('/aggregate_data', methods=['GET'])
def get_aggregated_data():
    recipes = recipe_dao.get_all_recipes()

    filtered_recipes = list(filter(lambda recipe: "Mehl" in recipe.ingredients, recipes))

    titles_lowercase = list(map(lambda recipe: recipe.title.lower(), filtered_recipes))

    total_steps = reduce(lambda acc, recipe: acc + len(recipe.steps.split()), filtered_recipes, 0)

    return jsonify({
        'titles_lowercase': titles_lowercase,
        'total_steps': total_steps
    }), 200