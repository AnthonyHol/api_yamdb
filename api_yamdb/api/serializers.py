import datetime as dt
from rest_framework import serializers
from reviews.models import User, Category, Genre, Title, Review, Comment


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "bio",
        )


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "confirmation_code")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("title", "text", "pub_date")


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = "__all__"

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError("Год указан неправильно")
        return value