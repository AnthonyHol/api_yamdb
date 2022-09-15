from django.contrib import admin

from .models import (Genre, Category, Comment, 
                    Review, Title, User)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date')
    search_fields = ('text',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'score', 'pub_date')
    search_fields = ('text',)

@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category', 'description')
    search_fields = ('name',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role")
    empty_value_display = "-пусто-"    
"""
@admin.register(TitleGenre)
class TitleGenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title_id', 'genre_id')
    search_fields = ('title_id', 'genre_id',)
"""
