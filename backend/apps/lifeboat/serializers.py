from rest_framework import serializers

from apps.graveyard.models import Category

from .models import Listing, Offer, SavedSearch


class ListingListSerializer(serializers.ModelSerializer):
    """C4 card: hides seller identity on stealth listings (L-08)."""

    category = serializers.SlugRelatedField(slug_field="slug", read_only=True)
    display_title = serializers.SerializerMethodField()
    seller_username = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = (
            "id", "display_title", "category", "pricing_mode", "price",
            "metrics", "urgency_score", "verified", "stealth", "seller_username",
            "created_at",
        )

    def get_display_title(self, obj) -> str:
        return obj.stealth_title if obj.stealth else obj.title

    def get_seller_username(self, obj):
        if obj.stealth:
            return None
        return obj.seller.username


class ListingDetailSerializer(ListingListSerializer):
    """C5 due-diligence view. Stealth identity stays masked unless the viewer
    has made an offer (US-3.5 blind-contact rule)."""

    asset_types = serializers.SerializerMethodField()
    days_on_market = serializers.SerializerMethodField()

    class Meta(ListingListSerializer.Meta):
        fields = ListingListSerializer.Meta.fields + (
            "pitch", "asset_types", "tech_stack", "runway_months",
            "status", "expires_at", "days_on_market",
        )

    def get_asset_types(self, obj):
        return [obj.AssetType(a).label for a in obj.asset_types]

    def get_days_on_market(self, obj) -> int:
        from django.utils import timezone

        return (timezone.now() - obj.created_at).days


class ListingCreateSerializer(serializers.ModelSerializer):
    """US-3.1–3.3 — the 5-step listing wizard payload. Category by slug."""

    category = serializers.SlugRelatedField(slug_field="slug", queryset=Category.objects.all())

    class Meta:
        model = Listing
        fields = (
            "id", "title", "category", "pitch", "asset_types", "pricing_mode",
            "price", "metrics", "runway_months", "stealth", "tech_stack",
        )
        read_only_fields = ("id",)

    def validate(self, attrs):
        if attrs.get("pricing_mode") == "fixed" and not attrs.get("price"):
            raise serializers.ValidationError("Fixed price requires a price.")
        return attrs


class OfferSerializer(serializers.ModelSerializer):
    buyer_username = serializers.CharField(source="buyer.username", read_only=True)

    class Meta:
        model = Offer
        fields = ("id", "listing", "buyer_username", "amount", "message", "status", "created_at")
        read_only_fields = ("listing", "status")


class SavedSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedSearch
        fields = ("id", "filters", "alert_channel", "created_at")
        read_only_fields = ("user",)
