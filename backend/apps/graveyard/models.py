from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.text import slugify


class NamedModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(NamedModel):
    """Product category (chatbots, hardware, video, ...)."""


class CauseOfDeath(NamedModel):
    """Why projects die (competition, no PMF, legal, ...)."""


class Grave(models.Model):
    """G-01/G-08 — a tombstone for one dead/dying AI project."""

    class Status(models.TextChoices):
        DEAD = "dead", "Dead"
        PIVOTED = "pivoted", "Pivoted"
        ABSORBED = "absorbed", "Absorbed"
        DELAYED = "delayed", "Delayed"
        ROLLBACK = "rollback", "Rollback"
        UNCONFIRMED = "unconfirmed", "Unconfirmed"  # US-2.3

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    summary = models.CharField(max_length=300, help_text="One-line summary")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DEAD)
    born_on = models.DateField(null=True, blank=True)
    died_on = models.DateField(null=True, blank=True)
    funding_raised = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    region = models.CharField(max_length=60, blank=True, default="")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="graves")
    cause = models.ForeignKey(CauseOfDeath, on_delete=models.SET_NULL, null=True, blank=True, related_name="graves")
    narrative = models.TextField(blank=True, help_text="The autopsy — what happened and what we learned")
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-died_on", "-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def is_counted_in_stats(self) -> bool:
        """BR-01/US-2.3: unconfirmed entries are excluded from the stats dashboard."""
        return self.status != self.Status.UNCONFIRMED


class Source(models.Model):
    """BR-01 — verifiable evidence for a grave entry."""

    grave = models.ForeignKey(Grave, on_delete=models.CASCADE, related_name="sources")
    url = models.URLField()
    title = models.CharField(max_length=300)
    published_on = models.DateField(null=True, blank=True)


class Submission(models.Model):
    """US-2.1/US-2.2 — community-reported deaths awaiting moderation (48h SLA)."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="submissions", null=True, blank=True)
    payload = models.JSONField(help_text="name, url, category, status, shutdown date, evidence link, context")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    moderator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="moderated_submissions")
    reject_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]


class Reaction(models.Model):
    """US-1.5 — one candle per user per grave."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reactions")
    grave = models.ForeignKey(Grave, on_delete=models.CASCADE, related_name="reactions")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "grave"], name="unique_candle_per_user"),
        ]


class Comment(models.Model):
    """US-1.5 — tombstone comments."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    grave = models.ForeignKey(Grave, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
