from pydantic import UUID4
from food.models import *
from ninja import Schema, ModelSchema
from datetime import date
from ninja.orm import create_schema
from typing import List

ingredientschema = create_schema(Ingredient, depth=1)
ass = create_schema(Recipe, depth = 2)
class UUIDSchema(Schema):
    id: UUID4
class SpeciesOut(Schema):
    id: UUID4
    name: str
class IngredientSchema(Schema):
    name:str
    measure: str
    calories: float

class IngredientOut(IngredientSchema):
    id: UUID4
    ingredient_type: SpeciesOut

class ItemOut(UUIDSchema):
    ingredient: IngredientOut
    amount: int
    note: str

class IngredientChecker(Schema):
    name: str
    measure: str
class ItemIn(Schema):
    amount: float
    note: str
class RecipeTypeOut(Schema):
    id: UUID4
    name: str
class RecipeSchema(Schema):
    name: str
    duration: int
    recipe_description: str
    serving: int

class RecipeSchemaIn(RecipeSchema):
    pass

class RecipeSchemaOut(RecipeSchema):
    id: UUID4
    recipe_type: RecipeTypeOut= None
    recipe_ingredient: List[ItemOut]
    total_calories: float = None
    total_carbs: int = None

class DailySchemaOut(Schema):
    recipe: List[RecipeSchemaOut]
    total_calories: int
    intake_calories: int
    status: str

class DailySchemaIn(Schema):
    recipe: UUID4
    total_calories: int
    intake_calories: int
    status: str
DailyScehmas = create_schema(Daily_intake, depth = 1)