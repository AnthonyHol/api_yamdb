from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import SimpleRouter

from .views import APIGetToken, APISignUp, UsersViewSet

router = SimpleRouter()

router.register("users", UsersViewSet, basename="users")

urlpatterns = [
    path("v1/", include(router.urls), name="v1"),
    path("v1/auth/token/", APIGetToken.as_view(), name="get_token"),
    path("v1/auth/signup/", APISignUp.as_view(), name="sign_up_token"),
]
