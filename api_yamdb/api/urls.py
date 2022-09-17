# from macpath import basename
from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet)
from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import SimpleRouter

from .views import APIGetToken, APISignUp, UsersViewSet

# router = SimpleRouter()
router = routers.DefaultRouter()

router.register('users', UsersViewSet, basename='users')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', 
                CommentViewSet, basename='comments')
router.register(r'titles/(?P<title_id>\d+)/reviews', 
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)',
                ReviewViewSet, basename='review-detail')
router.register('titles', TitleViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)


urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/token/", APIGetToken.as_view(), name="get_token"),
    path("v1/auth/signup/", APISignUp.as_view(), name="sign_up_token"),
]
