from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  calorie_goal = models.IntegerField(default=0)
  protein_goal = models.IntegerField(default=0)
  carbs_goal = models.IntegerField(default=0)
  fat_goal = models.IntegerField(default=0)

  # def calculate_calorie_goal(self):
  #   calorie_goal = (self.protein_goal * 4) + (self.protein_carbs * 4) + (self.protein_goal * 4)

  def get_absolute_url(self):
    return reverse('profile_page')

class Food(models.Model):
  name = models.CharField(max_length=100)
  food_id = models.CharField(max_length=500)
  protein = models.IntegerField()
  carbs = models.IntegerField()
  fat = models.IntegerField()
  calories = models.IntegerField()
  serving = models.IntegerField()
  brand = models.CharField(max_length=100)

  def __str__(self):
    return f'{self.name} {self.food_id}'
    
class Meal(models.Model):
  breakfast = models.ManyToManyField(Food, blank=True, related_name='breakfast')
  lunch = models.ManyToManyField(Food, blank=True, related_name='lunch')
  dinner = models.ManyToManyField(Food, blank=True, related_name='dinner')
  calories = models.IntegerField(default=0)
  carbs = models.IntegerField(default=0)
  protein = models.IntegerField(default=0)
  fat = models.IntegerField(default=0)
  date = models.DateField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  def __str__(self):
    return f'{self.date} {self.user}'
  
  def calculate_nutrients(self):
    breakfast = []
    lunch = []
    dinner = []
    for item in self.food_items.filter(category='breakfast'):
      name = item.food.name
      id = item.food.id
      calories = item.food.calories * (item.quantity / 100)
      protein = item.food.protein * (item.quantity / 100)
      carbs = item.food.carbs * (item.quantity / 100)
      fat = item.food.fat * (item.quantity / 100)
      breakfast.append(
        {'name': name,
         'id': id,
         'quantity': item.quantity,
         'calories': calories, 
         'protein': protein, 
         'carbs': carbs, 
         'fat': fat 
         }
      )

    for item in self.food_items.filter(category='lunch'):
      name = item.food.name
      id = item.food.id
      calories = item.food.calories * (item.quantity / 100)
      protein = item.food.protein * (item.quantity / 100)
      carbs = item.food.carbs * (item.quantity / 100)
      fat = item.food.fat * (item.quantity / 100)
      lunch.append(
        {'name': name,
         'id': id,
         'quantity': item.quantity,
         'calories': calories, 
         'protein': protein, 
         'carbs': carbs, 
         'fat': fat 
         }
      )

    for item in self.food_items.filter(category='dinner'):
      name = item.food.name
      id = item.food.id
      calories = item.food.calories * (item.quantity / 100)
      protein = item.food.protein * (item.quantity / 100)
      carbs = item.food.carbs * (item.quantity / 100)
      fat = item.food.fat * (item.quantity / 100)
      dinner.append(
        {'name': name,
         'id': id,
         'quantity': item.quantity,
         'calories': calories, 
         'protein': protein, 
         'carbs': carbs, 
         'fat': fat 
         }
      )

    return [breakfast, lunch, dinner]
    print(self.food_items)
  
  def calculate_remaining_nutrients(self):
    user = User.objects.get(id=self.user.id)
    profile = Profile.objects.get(user=user)
    remaining_calories = profile.calorie_goal - self.calories
    remaining_protein = profile.protein_goal - self.protein
    remaining_carbs = profile.carbs_goal - self.carbs
    remaining_fat =  profile.fat_goal - self.fat

    return {
      'calories': remaining_calories,
      'protein': remaining_protein,
      'carbs': remaining_carbs,
      'fat': remaining_fat,
    }

class MealFood(models.Model):
  meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='food_items' )
  food = models.ForeignKey(Food, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=0)
  category = models.CharField(max_length=100)