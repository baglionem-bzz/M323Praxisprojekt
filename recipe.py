from dataclasses import dataclass

@dataclass
class Recipe:
    id: int
    title: str
    ingredients: str
    steps: str
