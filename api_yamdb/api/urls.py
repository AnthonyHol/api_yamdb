from django.urls import include, path
from rest_framework.routers import SimpleRouter
from api.views import CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet

from .views import APIGetToken, APISignUp, UsersViewSet

router = SimpleRouter()

router.register("users", UsersViewSet, basename="users")
router.register('titles', TitleViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/token/", APIGetToken.as_view(), name="get_token"),
    path("v1/auth/signup/", APISignUp.as_view(), name="sign_up_token"),
]
