from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
# from django.db.models import get_or_create
from .models import Food, Meal, MealFood, Profile
import requests 
import os
from datetime import date
from .forms import CustomUserCreationForm


# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = CustomUserCreationForm()
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
  quantity = int(request.POST.__getitem__('quantity')) 
  food = Food.objects.get(id=food_id)
  selectedDate = request.POST.__getitem__('date')
  try: 
    meal = Meal.objects.get(date=selectedDate, user=request.user)

  except Meal.DoesNotExist:
    meal = Meal.objects.create(
      date = selectedDate,
      user = request.user
    )


  if category == 'breakfast':
    meal.breakfast.add(food_id)

  elif category == 'lunch':
    meal.lunch.add(food_id)

  elif category == 'dinner':
    meal.dinner.add(food_id)

  meal.calories += food.calories * (quantity / 100)
  meal.protein += food.protein * (quantity / 100)
  meal.carbs += food.carbs * (quantity / 100) 
  meal.fat += food.fat * (quantity / 100)
  meal.save()
  try: 
    meal_food = MealFood.objects.get(meal = meal, food = food, category = category)

  except MealFood.DoesNotExist:
    meal_food = MealFood.objects.create(meal = meal, food = food, category = category)
  meal_food.quantity += quantity
  meal_food.save()
  return redirect('food_details', food.food_id)

def unassoc_food(request, meal_id, food_id, category):
  meal = Meal.objects.get(id=meal_id, user=request.user)
  food = Food.objects.get(id=food_id)
  meal_food = MealFood.objects.get(meal=meal, food=food, category=category)
  quantity = meal_food.quantity
  if category == 'breakfast':
    meal.breakfast.remove(food_id)
  elif category == 'lunch':
    meal.lunch.remove(food_id)
  elif category == 'dinner':
    meal.dinner.remove(food_id)
  meal_food.delete()
  meal.calories -= food.calories * (quantity / 100)
  meal.carbs -= food.carbs * (quantity / 100)
  meal.protein -= food.protein * (quantity / 100)
  meal.fat -= food.fat * (quantity / 100)
  meal.save()
  redirect_url = reverse('meal_detail')
  redirect_url += f"?date={meal.date}"
  return redirect(redirect_url)

def meal_detail(request):
  selected_date = request.GET.get('date', '')
  try: 
    meal = Meal.objects.get(date=selected_date, user=request.user)
  except Meal.DoesNotExist:
    meal = Meal.objects.create(
      date = selected_date,
      user = request.user
    )
  breakfast = meal.calculate_nutrients()[0]
  lunch = meal.calculate_nutrients()[1]
  dinner = meal.calculate_nutrients()[2]
  remaining = meal.calculate_remaining_nutrients()
  return render(request, 'meals/meal_detail.html', {'breakfast': breakfast, 'lunch': lunch, 'dinner': dinner, 'meal':meal, 'remaining': remaining})

def profile_page(request):
  user = request.user
  profile = Profile.objects.get(user=user)
  return render(request, 'profiles/profile_page.html', {'user': user, 'profile': profile})
  
class UpdateProfile(UpdateView):
  model = Profile
  fields = ['calorie_goal', 'protein_goal', 'carbs_goal', 'fat_goal',]

