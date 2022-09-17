from api.permissons import IsAdmin, IsAdminOrReadOnly
from api.serializers import (CategorySerializer, CommentSerializer,
                             GetTokenSerializer, ReviewSerializer,
                             SignUpSerializer, TitleSerializer,
                             UsersSerializer)
from django.core.exceptions import SuspiciousOperation
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title, User


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
    """
    Вьюсет для объекта обзора.
    Просмотр, создание,  редактирование, удаление.
    """

    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        pk = self.kwargs.get("pk")
        if not Review.objects.filter(title_id=title_id).exists():
            raise NotFound(
                    detail="Произведение не найдено",
                    code=404)
        if pk and not Review.objects.filter(id=pk).exists():
            raise NotFound(
                    detail="Отзыв не найден",
                    code=404)
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        title_id = self.request.data.get("title_id")
        text = self.request.data.get("text")
        score = self.request.data.get("score")
        token = GetTokenSerializer(data=self.request.data)
        token.is_valid(raise_exception=True)
        if title_id is not None and text is not None and score is not None:
            if not Title.objects.get(title_id=title_id).exists():
                raise ParseError(
                    detail="Не найдено произведение!",
                    code=404)
            if not title_id.isnumeric():
                raise ParseError(
                    detail="Поле title_id должно быть числовым!",
                    code=400)
            if not score.isnumeric():
                raise ParseError(
                    detail="Поле рейтинг должно быть цифровым!",
                    code=400)
            if 0 > score > 10:
                raise ParseError(
                    detail="Рейтинг должен лежать в диапазоне 0-10!",
                    code=400)
            serializer.save(
                    title_id=title_id,
                    text=text,
                    score=score,
                    author=self.request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            raise ParseError(
                    detail="Отсутствует одно из обязательных полей!",
                    code=400)

    def partial_update(self, request, title_id, review_id):
        title = get_object_or_404(Title, id=title_id)
        review = get_object_or_404(Review, title=title_id, id=review_id)
        cur_user = request.user
        cur_user_group = cur_user.groups()
        token = GetTokenSerializer(data=request.data)
        token.is_valid(raise_exception=True)
        review_author = review.author
        if 'user' in cur_user_group and cur_user != review_author:
            return Response("У вас нет полномочий "
                            "для редактирования обзора",
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(
                    review,
                    data=self.request.data,
                    partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, title_id, review_id):
        title = get_object_or_404(Title, id=title_id)
        review = get_object_or_404(Review, id=review_id, title=title_id)
        cur_user = request.user
        cur_user_group = cur_user.groups()
        review_author = review.author
        token = GetTokenSerializer(data=request.data)
        token.is_valid(raise_exception=True)
        if 'user' in cur_user_group and cur_user != review_author:
            return Response("У вас нет полномочий "
                            "для удаления обзора",
                            status=status.HTTP_403_FORBIDDEN)
        else:
            review.delete()
            return Response("Обзор удален",
                            status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для объекта комментарий.
    Просмотр, создание,  редактирование, удаление.
    """
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        comment_id = self.kwargs.get("pk")
        if not Review.objects.filter(id=review_id).exists():
            raise NotFound(
                    detail="Не найден отзыв",
                    code=404)
        if not Title.objects.filter(id=title_id).exists():
            raise NotFound(
                    detail="Не найдено произведение",
                    code=404)
        if comment_id and not Comment.objects.filter(id=comment_id).exists():
            raise NotFound(
                    detail="Комментарий не найден",
                    code=404)
        return Comment.objects.filter(review=review_id)

    def perform_create(self, serializer):
        title_id = self.request.data.get("title_id")
        review_id = self.request.data.get("review_id")
        text = self.request.data.get("text")
        token = GetTokenSerializer(data=self.request.data)
        token.is_valid(raise_exception=True)
        if title_id is not None:
            if not Title.objects.get(title_id=title_id).exists():
                raise ParseError(
                    detail="Не найдено произведение!",
                    code=404)
            if not Review.objects.get(title_id=title_id,
                                      review_id=review_id).exists():
                raise ParseError(
                    detail="Не найден обзор!",
                    code=404)
            if not title_id.isnumeric():
                raise ParseError(
                    detail="Поле title_id должно быть числовым!",
                    code=400)
            if not review_id.isnumeric():
                raise ParseError(
                    detail="Поле review_id должно быть числовым!",
                    code=400)
            serializer.save(
                    review_id=review_id,
                    text=text,
                    author=self.request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            raise ParseError(
                    detail="Отсутствует одно из обязательных полей!",
                    code=400)

    def partial_update(self, request, title_id, review_id, comment_id):
        title = get_object_or_404(Title, id=title_id)
        review = get_object_or_404(Review, title=title_id, id=review_id)
        comment = get_object_or_404(Comment,
                                    review_id=review_id,
                                    id=comment_id)
        cur_user = request.user
        cur_user_group = cur_user.groups()
        token = GetTokenSerializer(data=request.data)
        token.is_valid(raise_exception=True)
        comment_author = comment.author
        if 'user' in cur_user_group and cur_user != comment_author:
            return Response("У вас нет полномочий "
                            "для редактирования комментария",
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(
                    comment,
                    data=self.request.data,
                    partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, title_id, review_id, comment_id):
        title = get_object_or_404(Title, id=title_id)
        rewiew = get_object_or_404(Review, id=review_id, title=title_id)
        comment = get_object_or_404(Comment, id=comment_id)
        cur_user = request.user
        cur_user_group = cur_user.groups()
        comment_author = comment.author
        token = GetTokenSerializer(data=request.data)
        token.is_valid(raise_exception=True)
        if 'user' in cur_user_group and cur_user != comment_author:
            return Response("У вас нет полномочий "
                            "для удаления комментария",
                            status=status.HTTP_403_FORBIDDEN)
        else:
            comment.delete()
            return Response("Комментарий удален",
                            status=status.HTTP_204_NO_CONTENT)
