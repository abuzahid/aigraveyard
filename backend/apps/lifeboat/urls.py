from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ListingViewSet, OfferListCreateView, SavedSearchViewSet

router = DefaultRouter()
router.register("listings", ListingViewSet, basename="listing")
router.register("saved-searches", SavedSearchViewSet, basename="saved-search")

urlpatterns = [
    path("listings/<int:listing_pk>/offers/", OfferListCreateView.as_view(), name="listing-offers"),
    path("", include(router.urls)),
]
