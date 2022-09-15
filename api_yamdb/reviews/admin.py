from django.contrib import admin

# Register your models here.
from .models import Category, Genre, Title

admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)