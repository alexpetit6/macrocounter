from django.urls import path
from . import views
	
urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('accounts/signup/', views.signup, name='signup'),
  path('foods/search', views.search_food, name='search_food'),
  path('foods/food_details/<str:food_id>/', views.food_details, name='food_details'),
  path('foods/<int:food_id>/assoc_food/', views.assoc_food, name='assoc_food'),
  path('meals/', views.meal_detail, name='meal_detail'),
  path('meals/<int:meal_id>/unassoc_food/<int:food_id>/<str:category>', views.unassoc_food, name='unassoc_food'),
  path('profile/', views.profile_page, name='profile_page'),
  path('profile/<int:pk>/update', views.UpdateProfile.as_view(), name='update_profile')
]