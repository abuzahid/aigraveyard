from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets

from apps.core.events import publish_event

from .models import Listing, Offer, SavedSearch
from .serializers import (
    ListingCreateSerializer,
    ListingDetailSerializer,
    ListingListSerializer,
    OfferSerializer,
    SavedSearchSerializer,
)


class ListingViewSet(viewsets.ModelViewSet):
    """L-03/US-4.1 — browse the Lifeboat. Filters: category, max_price,
    min_urgency, verified, q."""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Listing.objects.select_related("seller", "category").filter(status=Listing.Status.ACTIVE)
        p = self.request.query_params
        if category := p.get("category"):
            qs = qs.filter(category__slug=category)
        if max_price := p.get("max_price"):
            qs = qs.filter(price__lte=max_price)
        if min_urgency := p.get("min_urgency"):
            qs = qs.filter(urgency_score__gte=min_urgency)
        if p.get("verified") in ("1", "true"):
            qs = qs.filter(verified=True)
        if q := p.get("q"):
            qs = qs.filter(title__icontains=q)
        return qs

    def get_serializer_class(self):
        if self.action == "create":
            return ListingCreateSerializer
        if self.action == "retrieve":
            return ListingDetailSerializer
        return ListingListSerializer

    def perform_create(self, serializer):
        listing = serializer.save(seller=self.request.user)
        publish_event(
            "listing.new",
            {"id": listing.id, "title": listing.stealth_title if listing.stealth else listing.title},
        )
        # US-4.3 — async saved-search alert dispatch
        from .tasks import dispatch_savedsearch_alerts

        dispatch_savedsearch_alerts.delay(listing.id)


class OfferListCreateView(generics.ListCreateAPIView):
    """US-3.6/US-4.2 — private offers. Buyers see their own; sellers see
    offers on their listings."""

    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Offer.objects.filter(
            listing_id=self.kwargs["listing_pk"]
        ).select_related("buyer", "listing", "listing__seller").filter(
            buyer=self.request.user
        ) | Offer.objects.filter(listing_id=self.kwargs["listing_pk"], listing__seller=self.request.user)

    def perform_create(self, serializer):
        listing = get_object_or_404(Listing, pk=self.kwargs["listing_pk"], status=Listing.Status.ACTIVE)
        offer = serializer.save(buyer=self.request.user, listing=listing)
        # Redis pub/sub -> Node -> seller's WebSocket room (D2 event flow)
        publish_event(
            "offer.new",
            {
                "offer_id": offer.id,
                "listing_id": listing.id,
                "listing_title": listing.title,
                "amount": str(offer.amount),
                "seller_id": listing.seller_id,
                "buyer_username": self.request.user.username,
            },
        )


class SavedSearchViewSet(viewsets.ModelViewSet):
    """US-4.3 — saved searches & alerts (own records only)."""

    serializer_class = SavedSearchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedSearch.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
