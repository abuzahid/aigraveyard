from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase

from apps.graveyard.tests import make_grave
from apps.lifeboat.models import Listing

from .tasks import send_weekly_digest

User = get_user_model()


class DigestTests(TestCase):
    def test_digest_email_content_and_recipients(self):
        subscriber = User.objects.create_user(
            "reader", email="reader@example.com"
        )  # notify_digest defaults True
        User.objects.create_user("muted", email="muted@example.com", notify_digest=False)

        make_grave("FreshDead")  # created now -> within the week window
        seller = User.objects.create_user("seller")
        Listing.objects.create(
            seller=seller,
            title="SinkingShip",
            category=make_category(),
            pitch="x",
            asset_types=["codebase"],
            pricing_mode="offer",
            metrics={"mrr": 2000},
            runway_months=2,
        )

        result = send_weekly_digest()

        self.assertEqual(result["graves"], 1)
        self.assertEqual(result["sinking"], 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["reader@example.com"])
        self.assertIn("FreshDead", mail.outbox[0].body)
        self.assertIn("SinkingShip", mail.outbox[0].body)


from apps.graveyard.models import Category  # noqa: E402


def make_category():
    return Category.objects.get_or_create(name="Digest", defaults={"slug": "digest"})[0]
