import uuid
from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.fields import IntegerField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.utils import timezone
from config.utils.models import Entity
from django.db.models import Avg, Min, Sum
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()
class Recipe(Entity):
    user = models.ForeignKey(User, null=True, blank=True, verbose_name='user', on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, default='')
    photo = models.ImageField(upload_to='recipes/', null=True, blank=True)
    recipe_ingredient = models.ManyToManyField('Item', verbose_name='items', related_name='recipe')
    recipe_type = models.ForeignKey("RecipeType", blank=True , null= True  ,on_delete=models.SET_NULL)
    duration = models.IntegerField(null = True , blank= True)
    time_of_create = models.DateField(default = timezone.now)
    recipe_description = models.TextField(default = '')
    total_calories = models.DecimalField(blank=True , null=True, decimal_places=3 , max_digits=8 )
    total_carbs = models.IntegerField(blank=True, null=True)
    serving = models.IntegerField(blank = True, null= True)
    posted = models.BooleanField(blank=True , null=True, default=False)
    @property
    def total_cal(self):
        total_cal = sum(
            i.ingredient.calories * i.amount for i in self.recipe_ingredient.all()
        )
        total_cal = total_cal/self.serving
        self.total_calories = total_cal
        return self.total_calories
    def __str__(self):
        return f" {self.total_cal} {self.name} {self.id} "

class Ingredient(Entity):
    name = models.CharField(max_length=255)
    ingredient_type = models.ForeignKey('Species', on_delete=models.SET_NULL, related_name="ingrident_species",
                                        null=True, blank=True)
    gram = 'gram'
    tbsp = 'tbsp'
    tsp = 'tsp'
    cup = 'cup'
    single = 'single'
    measure = models.CharField('title', max_length=255, choices=[
        (gram, gram),
        (tbsp, tbsp),
        (cup, cup),
        (single, single),
    ])
    calories = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=3)

    def __str__(self):
        return f" {self.name} {self.id} "
class Item(Entity):
    user = models.ForeignKey(User, null=True, blank=True, verbose_name='user', on_delete=models.SET_NULL)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.SET_NULL, null= True, blank=True)
    amount = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=3)
    note = models.CharField(max_length=255, default='')
    posted = models.BooleanField(null = True , blank=True , default = False)

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'
class Species(Entity):
    name =  models.CharField(max_length=255, default='')

    def __str__(self):
        return f" {self.name} {self.id} "



class RecipeType(Entity):
    name =  models.CharField(max_length=255, default='')

    def __str__(self):
        return f" {self.name} {self.id} "

class Daily_intake(Entity):
    user = models.ForeignKey(User, null=True, blank=True, verbose_name='user', on_delete=models.SET_NULL)
    recipe = models.ManyToManyField(Recipe)
    total_calories = models.IntegerField(null=True , blank=True)
    intake_calories = models.IntegerField(null = True , blank= True)
    maintain = 'maintain'
    mild = 'mild'
    lose = 'lose'
    overlose = 'overlose'
    exceed = 'exceed'
    status = models.CharField('title', max_length=255, choices=[
        (maintain, maintain),
        (mild, mild),
        (lose, lose),
        (overlose, overlose),
        (exceed, exceed),
    ])

#class ship_recipe_ingredient(Entity):
#    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL , null=True , blank = True)
#    ingredient = models.ForeignKey(Ingredient, on_delete=models.SET_NULL , null=True , blank = True)
#    amount = models.IntegerField(null = True , blank= True)
#    note = models.CharField(max_length=255, default='')
