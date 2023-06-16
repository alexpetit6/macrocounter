from django.urls import path
from . import views
	
urlpatterns = [
  path('', views.home, name='home'),
  path('accounts/signup/', views.signup, name='signup'),
  path('foods/search', views.search_food, name='search_food'),
  path('meals/food_confirm_add', views.food_confirm_add, name='food_confirm_add'),
  
]