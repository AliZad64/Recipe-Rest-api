from django.contrib import admin
from .models import *
from easy_select2 import select2_modelform

class MembershipInline(admin.TabularInline):
    model = Recipe.recipe_ingredient.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [MembershipInline,]
    form = select2_modelform(Recipe)
    #list_display = ('user', 'name', 'photo', 'recipe_type', 'duration', 'time_of_create', 'recipe_description')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    # inlines = [TabularProperty]
    form = select2_modelform(Item)
    list_display = ('ingredient', 'amount', 'note')
admin.site.register(Ingredient)

admin.site.register(RecipeType)
admin.site.register(Species)
admin.site.register(Daily_intake)