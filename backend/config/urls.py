from django.contrib import admin
from django.urls import include, path

from apps.core.views import home_view
from apps.graveyard.views import GraveDetailView, candle_view

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("api/", include("apps.accounts.urls")),
    path("api/", include("apps.graveyard.urls")),
    path("api/", include("apps.lifeboat.urls")),
    path("api/", include("apps.analytics.urls")),
    path("graves/<slug:slug>/", GraveDetailView.as_view(), name="grave-detail"),
    path("graves/<slug:slug>/candle/", candle_view, name="grave-candle"),
    path("", home_view, name="home"),
]
