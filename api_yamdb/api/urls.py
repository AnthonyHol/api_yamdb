from api.views import CategoryViewSet, GenreViewSet, TitleViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('titles', TitleViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)

urlpatterns = [
    path("v1/", include(router.urls), name="v1"),
]
