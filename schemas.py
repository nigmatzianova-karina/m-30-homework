from typing import List

from pydantic import BaseModel


class BaseRecipe(BaseModel):
    name: str
    cook_time: int
    list_of_ingredients: str
    description: str


class RecipeIn(BaseRecipe):
    ...


class RecipeOut(BaseRecipe):
    id: int
    count_of_view: int

    class Config:
        from_attributes = True
