from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Role(models.TextChoices):
    READER = "reader", "Reader"
    FOUNDER = "founder", "Founder"
    BUYER = "buyer", "Buyer"


class User(AbstractUser):
    """User with multi-selectable roles (US-5.1) and notification prefs (US-5.3)."""

    roles = ArrayField(
        models.CharField(max_length=20, choices=Role.choices),
        default=list,
        blank=True,
        help_text="reader / founder / buyer (multi-select)",
    )
    # Notification preferences (US-5.3)
    notify_digest = models.BooleanField(default=True)
    notify_watchlist = models.BooleanField(default=True)
    notify_offers = models.BooleanField(default=True)

    def add_role(self, role: str) -> None:
        if role in Role.values and role not in self.roles:
            self.roles.append(role)
            self.save(update_fields=["roles"])
