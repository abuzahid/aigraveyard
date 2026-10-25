from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GraveViewSet, SubmissionCreateView

router = DefaultRouter()
router.register("graves", GraveViewSet, basename="grave")

urlpatterns = [
    path("graves/submit/", SubmissionCreateView.as_view(), name="submit-death"),
    path("", include(router.urls)),
]
