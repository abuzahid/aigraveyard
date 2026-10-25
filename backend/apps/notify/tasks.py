"""US-5.2 — the weekly 'Who Died This Week' + 'Sinking Ships to Save' digest."""
from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone


@shared_task
def send_weekly_digest():
    week_ago = timezone.now() - timedelta(days=7)

    from apps.graveyard.models import Grave
    from apps.lifeboat.models import Listing

    new_graves = Grave.objects.filter(created_at__gte=week_ago).order_by("-created_at")
    sinking = (
        Listing.objects.filter(status=Listing.Status.ACTIVE)
        .order_by("-urgency_score")[:3]
    )

    lines = ["WHO DIED THIS WEEK", "=" * 40]
    if new_graves:
        for grave in new_graves:
            lines.append(f"• {grave.name} ({grave.get_status_display()}) — {grave.summary}")
    else:
        lines.append("(a quiet week — no new graves)")

    lines += ["", "SINKING SHIPS TO SAVE", "=" * 40]
    if sinking:
        for listing in sinking:
            title = listing.stealth_title if listing.stealth else listing.title
            mrr = (listing.metrics or {}).get("mrr", "?")
            lines.append(f"• {title} — {mrr} MRR, ~{listing.urgency_score}% submerged")
    else:
        lines.append("(calm waters — no active listings)")

    subject = "🕯 AI Graveyard weekly digest"
    body = "\n".join(lines)

    recipients = list(
        get_user_model().objects.filter(is_active=True, notify_digest=True)
        .exclude(email="")
        .values_list("email", flat=True)
    )
    sent = 0
    for batch_start in range(0, len(recipients), 50):  # BCC batches of 50
        batch = recipients[batch_start : batch_start + 50]
        send_mail(subject, body, None, batch, fail_silently=True)
        sent += len(batch)
    return {"graves": new_graves.count(), "sinking": len(sinking), "emailed": sent}
