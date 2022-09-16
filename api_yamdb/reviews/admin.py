from django.contrib import admin

from .models import User, Category, Genre, Title


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role")
    empty_value_display = "-пусто-"


admin.site.register(User, UserAdmin, Genre, Category, Title)
