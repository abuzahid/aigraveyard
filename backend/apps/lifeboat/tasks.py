from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone


@shared_task
def expire_listings():
    """US-3.1 — listings expire after 60 days unless renewed."""
    from .models import Listing

    expired = Listing.objects.filter(status=Listing.Status.ACTIVE, expires_at__lt=timezone.now())
    return expired.update(status=Listing.Status.EXPIRED)


@shared_task
def dispatch_savedsearch_alerts(listing_id):
    """US-4.3 — when a new listing is created, notify buyers whose SavedSearch
    filters match. Email + realtime push (`alert.match` -> user room)."""
    from apps.core.events import publish_event
    from apps.graveyard.models import Category  # noqa: F401  (ensures app registry)

    from .models import Listing, SavedSearch

    try:
        listing = Listing.objects.select_related("seller", "category").get(pk=listing_id)
    except Listing.DoesNotExist:
        return

    for search in SavedSearch.objects.select_related("user").filter(user__notify_watchlist=True):
        if not _matches(listing, search.filters or {}):
            continue
        user = search.user
        publish_event(
            "alert.match",
            {"user_id": user.id, "listing_id": listing.id,
             "listing_title": listing.stealth_title if listing.stealth else listing.title},
        )
        if user.email:
            send_mail(
                subject=f"🌊 New Lifeboat match: {listing.title if not listing.stealth else listing.stealth_title}",
                message=(
                    f"A new sinking project matches your saved search:\n\n"
                    f"{listing.title if not listing.stealth else listing.stealth_title}\n"
                    f"Category: {listing.category.name}\n"
                    f"Metrics: {listing.metrics}\n"
                    f"View: /api/listings/{listing.id}/\n"
                ),
                from_email=None,
                recipient_list=[user.email],
                fail_silently=True,
            )
    return True


def _matches(listing, filters: dict) -> bool:
    """Filter keys: category (slug), max_price, min_mrr, tech_stack (any overlap)."""
    category = filters.get("category")
    if category and listing.category.slug != category:
        return False
    max_price = filters.get("max_price")
    if max_price is not None and (listing.price is None or float(listing.price) > float(max_price)):
        return False
    min_mrr = filters.get("min_mrr")
    if min_mrr is not None:
        mrr = (listing.metrics or {}).get("mrr")
        if mrr is None or float(mrr) < float(min_mrr):
            return False
    tech = filters.get("tech_stack") or []
    if tech and not set(tech) & set(listing.tech_stack or []):
        return False
    return True
