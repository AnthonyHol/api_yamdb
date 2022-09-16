from django.contrib import admin

from .models import User, Category, Genre, Title


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role")
    empty_value_display = "-пусто-"


class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    empty_value_display = "-пусто-"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    empty_value_display = "-пусто-"


class TitleAdmin(admin.ModelAdmin):
    list_display = ("name", "genre", "category")
    empty_value_display = "-пусто-"

admin.site.register(User, UserAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)