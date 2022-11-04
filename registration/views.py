from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from .serializers import(
    UserRegistrationSerializer,
    PasswordChangeSerializer,
    RecoveryPasswordSerializer,
    SetRecoveredPasswordSerializer,
)


User = get_user_model()


class RegistrationView(APIView):
    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request: Request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                'Thank for registration! Please activate your account',
                status=status.HTTP_201_CREATED
            )


class AccountActivationView(APIView):
    def get(self, request, activation_code):
        user = User.objects.filter(activation_code=activation_code).first()
        if not user:
            return Response(
                'Page not found',
                status=status.HTTP_404_NOT_FOUND
            )
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response(
            'Account activated! You can login now',
            status=status.HTTP_200_OK
        )


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'Password changed succsefully',
                status=status.HTTP_200_OK
            )

class RecoveryPasswordView(APIView):
    def post(self, request: Request):
        serializer = RecoveryPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_code()
            return Response(
                'Password recovery code has been send to your email',
                status=status.HTTP_200_OK
            )


class SetRecoveredPasswordView(APIView):
    def post(self, request: Request):
        serializer = SetRecoveredPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'Password recovered succsessfully',
                status=status.HTTP_200_OK
            )

class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request):
        username = request.user.username
        User.objects.filter(username=username).delete()
        return Response(
            'Account deleted succsessfully',
            status=status.HTTP_204_NO_CONTENT
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response(
            'Вы вышли из учетной записи. До свидания!',
            status=status.HTTP_200_OK
        )