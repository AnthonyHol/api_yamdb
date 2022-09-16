from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import APIGetToken, APISignUp, UsersViewSet

router = DefaultRouter()

router.register("users", UsersViewSet, basename="users")

urlpatterns = [
    path("v1/", include(router.urls), name="v1"),
    path("v1/auth/token/", APIGetToken.as_view(), name="get_token"),
    path("v1/auth/signup/", APISignUp.as_view(), name="sign_up_token"),
]
