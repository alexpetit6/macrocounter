# Generated by Django 4.2.2 on 2023-06-21 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_meal_calories_meal_carbs_meal_fat_meal_protein'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mealfood',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]