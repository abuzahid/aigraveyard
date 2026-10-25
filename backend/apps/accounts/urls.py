from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import MeView, RegisterView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/token/", obtain_auth_token, name="obtain-token"),
    path("auth/me/", MeView.as_view(), name="me"),
]
