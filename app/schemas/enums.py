from __future__ import annotations

from enum import Enum


class MealType(str, Enum):
    Morning = "Morning"
    Lunch = "Lunch"
    Dinner = "Dinner"
    Snack = "Snack"


class ArticleCategory(str, Enum):
    Recommended = "Recommended"
    Diet = "Diet"
    Beauty = "Beauty"
    Health = "Health"


