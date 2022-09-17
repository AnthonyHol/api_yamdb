from django.contrib import admin

from .models import Title, User, Review, Comment

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role")
    empty_value_display = "-пусто-"

class ReviewAdmin(admin.ModelAdmin):
    list_display = ("text",)
    empty_value_display = "-пусто-"

class CommentAdmin(admin.ModelAdmin):
    list_display = ("text",)
    empty_value_display = "-пусто-"

class TitleAdmin(admin.ModelAdmin):
    list_display = ("name",)
    empty_value_display = "-пусто-"

admin.site.register(User, UserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Title, TitleAdmin)