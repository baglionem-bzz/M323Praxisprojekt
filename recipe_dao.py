import sqlite3
from recipe import Recipe

class RecipeDao:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS recipes (
                                id INTEGER PRIMARY KEY,
                                title TEXT NOT NULL,
                                ingredients TEXT NOT NULL,
                                steps TEXT NOT NULL)""")
        self.conn.commit()

    def add_recipe(self, recipe):
        self.cursor.execute('INSERT INTO recipes (title, ingredients, steps) VALUES (?, ?, ?)',
                            (recipe.title, recipe.ingredients, recipe.steps))
        self.conn.commit()

    def get_recipe(self, recipe_id):
        self.cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
        row = self.cursor.fetchone()
        if row:
            return Recipe(row[0], row[1], row[2], row[3])
        return None

    def get_all_recipes(self):
        self.cursor.execute("SELECT * FROM recipes")
        rows = self.cursor.fetchall()
        return [Recipe(row[0], row[1], row[2], row[3]) for row in rows]

    def update_recipe(self, recipe):
        self.cursor.execute("UPDATE recipes SET title = ?, ingredients = ?, steps = ? WHERE id = ?",
                            (recipe.title, recipe.ingredients, recipe.steps, recipe.id))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def delete_recipe(self, recipe_id):
        self.cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def execute_operation(self, operation, *args):
        """
        Führt eine übergebene Datenbankoperation aus und gibt das Ergebnis zurück.
        """
        return operation(*args)

