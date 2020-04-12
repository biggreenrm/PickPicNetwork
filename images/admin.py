from django.contrib import admin
from .models import Image


# Регистрация приложения "Image" в кабинете администратора
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "image", "created"]
    list_filter = ["created"]

