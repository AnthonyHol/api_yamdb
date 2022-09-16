from django.contrib import admin

# Register your models here.
from .models import Category, Genre, Title, Review, Comment, User

admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(User)