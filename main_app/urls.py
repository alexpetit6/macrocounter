from django.urls import path
from . import views
	
urlpatterns = [
  path('', views.home, name='home'),
  path('accounts/signup/', views.signup, name='signup'),
  path('foods/search', views.search_food, name='search_food'),
  path('foods/food_details/<str:food_id>/', views.food_details, name='food_details'),
  path('foods/<int:food_id>/assoc_food/', views.assoc_food, name='assoc_food'),
]