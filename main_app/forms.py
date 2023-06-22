from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
  calorie_goal = forms.IntegerField(label='Calorie goal is calculated by macros do NOT try to edit calorie goal', widget=forms.NumberInput(attrs={'id': 'daily_calories', 'readonly': True}))
  protein_goal = forms.IntegerField(widget=forms.NumberInput(attrs={'id': 'daily_protein'}))
  carbs_goal = forms.IntegerField(widget=forms.NumberInput(attrs={'id': 'daily_carbs'}))
  fat_goal = forms.IntegerField(widget=forms.NumberInput(attrs={'id': 'daily_fat'}))

  class Meta(UserCreationForm.Meta):
    model = User
    fields = UserCreationForm.Meta.fields + ('username', 'password1', 'password2', 'calorie_goal', 'protein_goal', 'carbs_goal', 'fat_goal')
    
  def save(self, commit=True):
    user = super().save(commit=False)
    user.save()
    data = self.cleaned_data
    profile = Profile.objects.create(
      user=user, 
      calorie_goal=data['calorie_goal'], 
      protein_goal=self.data['protein_goal'],
      carbs_goal=self.data['carbs_goal'],
      fat_goal=self.data['fat_goal']
    )
    profile.save()

    return user
