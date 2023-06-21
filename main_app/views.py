from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
# from django.db.models import get_or_create
from .models import Food, Meal
import requests 
import os
from datetime import date

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def search_food(request):
  if request.method == "GET":
    ingr = request.GET.get('ingr', '')
    url = 'https://api.edamam.com/api/food-database/v2/parser'
    params = {
      'app_id': os.environ['API_ID'],
      'app_key': os.environ['API_KEY'],
      'ingr': ingr,
      'nutrient-type': 'logging'
    }
    response = requests.get(url, params)

    data = response.json()
    search_results = data['hints']
    context = {
      'search_results': search_results,
      'ingr': ingr
    }

    return render(request, 'foods/index.html', context)

def food_details(request, food_id):
  try:
    food = Food.objects.get(food_id=food_id)
  except Food.DoesNotExist:
    url = 'https://api.edamam.com/api/food-database/v2/parser'
    ingr = food_id
    params = {
      'app_id': os.environ['API_ID'],
      'app_key': os.environ['API_KEY'],
      'ingr': ingr,
      'nutrient-type': 'logging'
    }
    response = requests.get(url, params)
    data = response.json()
    search_results = data['hints']

    results = search_results[0]
    food = Food.objects.create(
      name = results['food']['label'],
      food_id = ingr,
      protein = results['food']['nutrients']['PROCNT'],
      carbs = results['food']['nutrients']['CHOCDF'],
      fat = results['food']['nutrients']['FAT'],
      calories = results['food']['nutrients']['ENERC_KCAL'],
      serving = 1,
    )
 
  return render(request, 'foods/food_details.html', {'food': food})

def assoc_food(request, food_id):
  category = request.POST.__getitem__('category')
  quantity = int(request.POST.__getitem__('quantity')) / 100
  food = Food.objects.get(id=food_id)
  try: 
    meal = Meal.objects.get(date=date.today(), user=request.user)

  except Meal.DoesNotExist:
    meal = Meal.objects.create(
      date = date.today(),
      user = request.user
    )

  if category == 'breakfast':
    meal.breakfast.add(food_id)

  elif category == 'lunch':
    meal.lunch.add(food_id)

  elif category == 'dinner':
    meal.dinner.add(food_id)

  meal.calories += food.calories * quantity
  meal.protein += food.protein * quantity
  meal.carbs += food.carbs * quantity
  meal.fat += food.fat * quantity
  meal.save()

  return redirect('food_details', food.food_id)


