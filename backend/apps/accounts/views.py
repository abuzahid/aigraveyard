from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/ — create account, return DRF token immediately."""

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "roles": user.roles,
                "token": token.key,
            },
            status=status.HTTP_201_CREATED,
        )


class MeView(APIView):
    """GET /api/auth/me/ — used by clients (and the Node service) to verify
    a DRF token and identify the user."""

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(
            {
                "id": request.user.id,
                "username": request.user.username,
                "roles": request.user.roles,
            }
        )
