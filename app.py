from flask import Flask, render_template, request, redirect, url_for
from database import init_db, get_recipes
from models import Recipe
from functional_utils import filter_recipes_by_ingredient, get_recipe_titles, count_total_ingredients

app = Flask(__name__)

init_db()


@app.route('/')
def index():
    recipes = get_recipes()
    return render_template('index.html', recipes=recipes)


@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients'].split(',')
        steps = request.form['steps'].split(',')

        new_recipe = Recipe(title, ingredients, steps)
        new_recipe.save()
        return redirect(url_for('index'))
    return render_template('add_recipe.html')


@app.route('/recipes')
def show_recipes():
    ingredient = request.args.get('ingredient')
    recipes = get_recipes()

    if ingredient:
        recipes = filter_recipes_by_ingredient(recipes, ingredient)

    total_ingredients = count_total_ingredients(recipes)
    titles = get_recipe_titles(recipes)

    return render_template('recipes.html', recipes=recipes, total_ingredients=total_ingredients, titles=titles)


if __name__ == '__main__':
    app.run(debug=True)
