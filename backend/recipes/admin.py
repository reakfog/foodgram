from django.contrib.admin import ModelAdmin, TabularInline, register

from .models import (Cart, Favorite, Following, Ingredient, IngredientRecipe,
                     Recipe, Tag)


@register(Tag)
class TagAdmin(ModelAdmin):
    ordering = ('color',)
    search_fields = ('name', 'slug',)


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    ordering = ('measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)


@register(IngredientRecipe)
class IngredientRecipeAdmin(ModelAdmin):
    ordering = ('ingredient',)
    search_fields = ('ingredient',)
    list_filter = ('ingredient',)


class RecipeIngredientInLine(TabularInline):
    model = Recipe.ingredients.through
    extra = 1


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    inlines = (RecipeIngredientInLine,)


@register(Following)
class FollowingAdmin(ModelAdmin):
    ordering = ('user',)
    search_fields = ('user',)
    list_filter = ('author',)


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    ordering = ('user',)
    search_fields = ('user',)
    list_filter = ('recipe',)


@register(Cart)
class CartAdmin(ModelAdmin):
    ordering = ('user',)
