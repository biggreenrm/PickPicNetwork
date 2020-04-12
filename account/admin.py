from django.contrib import admin
from .models import Profile

# Register your models here.

# Регистрация модели профиля для кабинета администратора
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "date_of_birth", "photo"]
