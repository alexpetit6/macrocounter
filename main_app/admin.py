from django.contrib import admin
from .models import Food, Meal, MealFood
# Register your models here.
admin.site.register(Food)
admin.site.register(Meal)
admin.site.register(MealFood)