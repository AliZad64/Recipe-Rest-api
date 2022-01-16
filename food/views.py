from django.shortcuts import render
from food.schemas import *
from ninja import Router , Form
from typing import List
from food.models import *
from account.models import *
from django.shortcuts import get_object_or_404
from pydantic import  UUID4
from config.utils.permissions import AuthBearer
from config.utils.schemas import MessageOut

recipe_controller = Router(tags=["recipes"])
ingredient_controller = Router(tags=["ingredients"])

@recipe_controller.get('ingredients/', response= List[ingredientschema])
def get_all_ingredients(request):
    return Ingredient.objects.all()

@recipe_controller.get('recipes/', response= List[RecipeSchemaOut])
def get_all_recipes(request):
    return Recipe.objects.all()

@recipe_controller.get('recipes/{id}', response= {200: RecipeSchemaOut})
def get_recipe(request, id: UUID4):
    return get_object_or_404(Recipe,id = id)

@recipe_controller.post('new_edit_recipe',auth=AuthBearer(), response=MessageOut)
def post_recipe(request,recipet: UUID4, payload: RecipeSchemaIn = Form(...)):
    user = get_object_or_404(User , id = request.auth.id)
    recipetype = get_object_or_404(RecipeType,id = recipet)
    recipe_check = Recipe.objects.filter(user = request.auth.id, posted=False)
    if recipe_check:
        return {'message': 'you already have unposted recipe'}
    recipe = Recipe.objects.create(**payload.dict(), recipe_type= recipetype, user = user)
    if recipe:
        return {'detail': 'created'}
    return {'detail': 'something went wrong try again'}

@recipe_controller.get('recipe_types',response= List[RecipeTypeOut])
def get_type_recipes(request):
    return RecipeType.objects.all()

@recipe_controller.post('add_edit_item', auth=AuthBearer(), response={201: MessageOut, 400:MessageOut })
def add_new_item(request, payload: ItemIn, id: UUID4):
    ingredient = get_object_or_404(Ingredient, id = id)

    recipe = get_object_or_404(Recipe,user = request.auth.id, posted = False)
    user_info = get_object_or_404(EmailAccount, id = request.auth.id)
    try:
        item = Item.objects.get(user = request.auth.id, ingredient= ingredient, posted= True, recipe= recipe)
        item.amount = payload.amount
        item.note = payload.note
        item.save()
    except Item.DoesNotExist:
        item = Item.objects.create(**payload.dict(), user = user_info, ingredient=ingredient , posted = True )
        recipe.recipe_ingredient.add(item)
    recipe.total_calories = recipe.total_cal
    recipe.save()
    return 201, {'message': 'created successfully'}

@recipe_controller.delete('delete_item/{id}', auth=AuthBearer(), response={203:MessageOut, 400:MessageOut})
def delete_item(request,id: UUID4 ):
    recipe = get_object_or_404(Recipe, user = request.auth.id, posted = False , recipe_ingredient__id = id)
    item = get_object_or_404(Item, id = id, user= request.auth.id, recipe__posted= False)
    item.delete()
    recipe.total_calories = recipe.total_cal
    recipe.save()
    return 203,{'message': 'item has been deleted'}


@recipe_controller.post('publish', auth=AuthBearer(), response={201: MessageOut, 400:MessageOut })
def publish_recipe(request):
    recipe = get_object_or_404(Recipe, user = request.auth.id, posted = False)
    recipe.posted = True
    recipe.save()
    return  201 , {'message': 'recipe has been posted'}


@recipe_controller.post('daily_list', auth=AuthBearer(), response={201:MessageOut, 400:MessageOut})
def add_daily(request, payload:DailySchemaIn):
    user = get_object_or_404(EmailAccount, id = request.auth.id)
    recipe = get_object_or_404(Recipe, id= payload.recipe)
    recipes = Recipe.objects.filter(id = payload.recipe)
    daily = Daily_intake.objects.filter(user = request.auth.id)
    if daily:
        daily.recipe.add(*recipes)
    else:
        daily = Daily_intake.objects.create(user = user,  total_calories=0 ,intake_calories=0,status = 'lose')
        daily.recipe.add(*recipes)
    daily = Daily_intake.objects.get(user = request.auth.id)
    if daily:
        daily.total_calories += recipe.total_calories
        daily.intake_calories = 500 + user.calorie_intake
        if daily.intake_calories - daily.total_calories <= daily.intake_calories/2:
            daily.status = 'overlose'
        elif daily.intake_calories - daily.total_calories <= user.calorie_intake:
            daily.status = 'lose'
        elif daily.intake_calories - daily.total_calories <= daily.intake_calories:
            daily.status = 'mild'
        else:
            daily.status = 'exceed'
        daily.save()
        return 201 , {'message': 'created'}
    return 400, {'message': 'something went wrong'}

@recipe_controller.get('dailylist/', auth=AuthBearer(), response=List[DailyScehmas])
def view_daily(request):
    return Daily_intake.objects.all()