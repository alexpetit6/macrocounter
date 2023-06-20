from django.db import models
from datetime import date
from django.contrib.auth.models import User
# Create your models here.

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
  date = models.DateField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  def __str__(self):
    return f'{self.date} {self.user}'