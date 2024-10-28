import sqlite3
from typing import List, Dict

def init_db():
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            steps TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_recipe(title: str, ingredients: str, steps: str):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO recipes (title, ingredients, steps)
        VALUES (?, ?, ?)
    ''', (title, ingredients, steps))
    conn.commit()
    conn.close()

def get_recipes() -> List[Dict[str, str]]:
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM recipes')
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "title": row[1], "ingredients": row[2], "steps": row[3]} for row in rows]
