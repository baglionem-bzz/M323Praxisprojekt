from database import save_recipe

class Recipe:
    def __init__(self, title: str, ingredients: list, steps: list):
        self.title = title
        self.ingredients = ', '.join(ingredients)
        self.steps = ', '.join(steps)

    def save(self):
        save_recipe(self.title, self.ingredients, self.steps)
