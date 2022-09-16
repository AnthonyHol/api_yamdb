from rest_framework import serializers
from reviews.models import User


class AdminsSerializer(serializers.ModelSerializer):
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


class UsersSerializer(serializers.ModelSerializer):
    class Meta(AdminsSerializer.Meta):
        read_only_fields = ("role",)


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username")
