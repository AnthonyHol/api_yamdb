from django.core.mail import send_mail
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import User, Category, Comment, Review, Genre, Title, Review

from api.permissons import IsAdmin, IsAdminOrReadOnly
from api.serializers import GetTokenSerializer, SignUpSerializer, UsersSerializer, CategorySerializer, TitleSerializer, ReviewSerializer

from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404


class UsersViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с пользователями.
    """

    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin,
    )
    lookup_field = "username"
    filter_backends = (SearchFilter,)
    search_fields = ("username",)

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path="me",
    )
    def get_current_user_info(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == "PATCH":
            serializer = UsersSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class APIGetToken(APIView):
    """
    APIView для получения токена.

    Запрос:
    {
        "username": имя пользователя(:obj:`string`),
        "confirmation_code": код доступа пользователя(:obj:`string`).
    }
    """

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data["username"])
        except User.DoesNotExist:
            return Response(
                {"username": "Такого пользователя не существует!"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if data.get("confirmation_code") == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response(
                {"token": str(token)}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"confirmation_code": "Неверный код подтверждения!"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class APISignUp(APIView):
    """
    APIView для получения кода доступа (его отправка на email).

    Запрос:
    {
        "username": имя пользователя(:obj:`string`),
        "email": электронная почта пользователя(:obj:`string`).
    }
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        send_mail(
            "Код для API",
            (
                f"Здравствуйте, {user.username}!\n"
                f"Код доступа к API: {user.confirmation_code}"
            ),
            "support_api@mail.com",
            [user.email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save()


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination

    def get_queryset(self):
            title_id = self.kwargs.get("title_id")
            review = get_object_or_404(Review, title_id=title_id)
            return review.objects.all()

    def perform_create(self, serializer):
        serializer.save()