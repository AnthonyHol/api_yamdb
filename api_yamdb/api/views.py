from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import User

from .permissons import IsAdmin
from .serializers import GetTokenSerializer, UsersSerializer


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
