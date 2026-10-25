from django.contrib import admin

from .models import Listing, Message, MessageThread, Offer, SavedSearch, Verification


class VerificationInline(admin.TabularInline):
    model = Verification
    extra = 0
    readonly_fields = ("decided_at",)


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    """US-6.2 — verify listings to grant the trust badge."""

    list_display = ("title", "seller", "status", "pricing_mode", "urgency_score", "verified", "expires_at")
    list_filter = ("status", "verified", "stealth", "category")
    search_fields = ("title", "pitch")
    inlines = [VerificationInline]
    actions = ["mark_verified", "mark_sold", "mark_rescued"]

    @admin.action(description="Mark selected listings as verified (applies badge + date)")
    def mark_verified(self, request, queryset):
        from django.utils import timezone

        for listing in queryset:
            Verification.objects.create(
                listing=listing,
                evidence_notes="Verified via admin action",
                verified_fields=["metrics"],
                admin=request.user,
            )
        queryset.update(verified=True, verified_at=timezone.now())

    @admin.action(description="Mark as sold")
    def mark_sold(self, request, queryset):
        queryset.update(status="sold")

    @admin.action(description="Mark as rescued (success story — BR-03)")
    def mark_rescued(self, request, queryset):
        queryset.update(status="rescued")


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("listing", "buyer", "amount", "status", "created_at")
    list_filter = ("status",)


admin.site.register(MessageThread)
admin.site.register(Message)
admin.site.register(SavedSearch)
