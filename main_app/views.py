from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Food, Meal
import requests

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
      'app_id': 'abb5c5e1',
      'app_key': '03d3763004f76acd1ca92034dce991b0',
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

def confirm_add_food(request, food_id):
  old_food = Food.objects.get(food_id)
  if old_food.food_id == food_id:
    return render('foods/confirm_add_food', {
      'food': old_food
    })
  else: 
    ingr = food_id
    url = 'https://api.edamam.com/api/food-database/v2/parser'
    params = {
      'app_id': 'abb5c5e1',
      'app_key': '03d3763004f76acd1ca92034dce991b0',
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

  return render(request, 'foods/confirm_add_food', context)

