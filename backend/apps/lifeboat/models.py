from datetime import timedelta

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from apps.graveyard.models import Category


class Listing(models.Model):
    """L-01/US-3.1 — a sinking project listed for rescue."""

    class AssetType(models.TextChoices):
        WHOLE_PRODUCT = "whole_product", "Whole product"
        CODEBASE = "codebase", "Codebase"
        DOMAIN_BRAND = "domain_brand", "Domain + brand"
        USER_BASE = "user_base", "User base"
        CUSTOMER_LIST = "customer_list", "Customer list"
        TEAM_HIRE = "team_hire", "Team hire"

    class PricingMode(models.TextChoices):
        FIXED = "fixed", "Fixed price"
        OFFER = "offer", "Make offer"
        GIVEAWAY = "giveaway", "Giveaway (free to a good home)"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        UNDER_AGREEMENT = "under_agreement", "Under agreement"
        SOLD = "sold", "Sold"
        RESCUED = "rescued", "Rescued"
        EXPIRED = "expired", "Expired"

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="listings")
    pitch = models.TextField(help_text="Seller narrative: why it's sinking, what works, what doesn't")
    asset_types = ArrayField(
        models.CharField(max_length=30, choices=AssetType.choices),
        default=list,
    )
    pricing_mode = models.CharField(max_length=20, choices=PricingMode.choices, default=PricingMode.OFFER)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    metrics = models.JSONField(
        default=dict,
        blank=True,
        help_text="{mrr, users, churn_pct, traffic_trend_pct} — disclosed by seller",
    )
    runway_months = models.PositiveIntegerField(null=True, blank=True, help_text="US-3.4 distress signal")
    urgency_score = models.PositiveSmallIntegerField(default=0, help_text="0-100 — the water level")
    stealth = models.BooleanField(default=False, help_text="L-08 anonymous listing")
    verified = models.BooleanField(default=False, help_text="L-06 metrics verified badge")
    verified_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    tech_stack = ArrayField(models.CharField(max_length=60), default=list, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True, help_text="Auto-set to +60 days on create (US-3.1)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-urgency_score", "-created_at"]

    def __str__(self):
        return self.stealth_title if self.stealth else self.title

    @property
    def stealth_title(self) -> str:
        return f"Stealth {self.category.name} — {self.metrics.get('mrr', '?')} MRR"

    def save(self, *args, **kwargs):
        # US-3.1: 60-day renewable window (only when not explicitly provided)
        if self._state.adding and self.expires_at is None:
            self.expires_at = timezone.now() + timedelta(days=60)
        # US-3.4: auto water level from runway when not set manually
        if self.runway_months and not self.urgency_score:
            self.urgency_score = max(0, min(100, 100 - self.runway_months * 10))
        super().save(*args, **kwargs)


class Verification(models.Model):
    """L-06/US-6.2 — evidence-based metric verification by an admin."""

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="verifications")
    evidence_notes = models.TextField(help_text="What was reviewed (analytics/statement screenshots, live access)")
    verified_fields = ArrayField(models.CharField(max_length=50), default=list)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="verifications")
    decided_at = models.DateTimeField(auto_now_add=True)


class MessageThread(models.Model):
    """L-04 — private buyer/seller conversation."""

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="threads", null=True, blank=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="threads")
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    thread = models.ForeignKey(MessageThread, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["created_at"]


class Offer(models.Model):
    """US-3.6/US-4.2 — private, non-binding offers (BR-04: platform is a venue)."""

    class Status(models.TextChoices):
        SENT = "sent", "Sent"
        ACCEPTED = "accepted", "Accepted"
        COUNTERED = "countered", "Countered"
        DECLINED = "declined", "Declined"

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="offers")
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="offers_made")
    thread = models.ForeignKey(MessageThread, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SENT)
    created_at = models.DateTimeField(auto_now_add=True)


class SavedSearch(models.Model):
    """US-4.3 — buyer alerts on matching new listings."""

    class Channel(models.TextChoices):
        INSTANT = "instant", "Instant"
        DIGEST = "digest", "Digest"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_searches")
    filters = models.JSONField(default=dict, help_text="{category, min_mrr, max_price, tech_stack}")
    alert_channel = models.CharField(max_length=10, choices=Channel.choices, default=Channel.INSTANT)
    created_at = models.DateTimeField(auto_now_add=True)
