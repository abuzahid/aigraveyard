from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.graveyard.models import Category

from .models import Listing, Offer, SavedSearch
from .tasks import _matches, expire_listings

User = get_user_model()


def make_category():
    return Category.objects.get_or_create(name="Productivity", defaults={"slug": "productivity"})[0]


class ListingAPITests(APITestCase):
    def setUp(self):
        self.seller = User.objects.create_user("seller", password="longpassword1")
        self.token = Token.objects.create(user=self.seller)
        self.auth = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}
        make_category()

    def test_create_requires_auth(self):
        resp = self.client.post("/api/listings/", {}, format="json")
        self.assertEqual(resp.status_code, 401)

    def test_create_sets_expiry_and_urgency(self):
        resp = self.client.post(
            "/api/listings/",
            {
                "title": "AI Notes App",
                "category": "productivity",
                "pitch": "12K users, no runway",
                "asset_types": ["codebase", "user_base"],
                "pricing_mode": "offer",
                "metrics": {"mrr": 1500, "users": 12000},
                "runway_months": 3,
            },
            format="json",
            **self.auth,
        )
        self.assertEqual(resp.status_code, 201)
        listing = Listing.objects.get(pk=resp.data["id"])
        self.assertEqual(listing.urgency_score, 70)  # 100 - 3*10 water level
        self.assertGreater(listing.expires_at, timezone.now() + timedelta(days=59))

    def test_fixed_price_requires_price(self):
        resp = self.client.post(
            "/api/listings/",
            {
                "title": "NoPrice",
                "category": "productivity",
                "pitch": "x",
                "asset_types": ["codebase"],
                "pricing_mode": "fixed",
            },
            format="json",
            **self.auth,
        )
        self.assertEqual(resp.status_code, 400)

    def test_stealth_masks_public_fields(self):
        listing = Listing.objects.create(
            seller=self.seller,
            title="SecretGPT",
            category=make_category(),
            pitch="x",
            asset_types=["codebase"],
            pricing_mode="offer",
            stealth=True,
        )
        resp = self.client.get("/api/listings/")
        entry = next(r for r in resp.data["results"] if r["id"] == listing.id)
        self.assertIsNone(entry["seller_username"])
        self.assertTrue(entry["display_title"].startswith("Stealth"))


class OfferTests(APITestCase):
    def setUp(self):
        self.seller = User.objects.create_user("seller")
        self.buyer = User.objects.create_user("buyer")
        self.listing = Listing.objects.create(
            seller=self.seller,
            title="SinkCo",
            category=make_category(),
            pitch="x",
            asset_types=["codebase"],
            pricing_mode="offer",
        )

    def auth(self, user):
        token = Token.objects.create(user=user)
        return {"HTTP_AUTHORIZATION": f"Token {token.key}"}

    def test_buyer_can_offer_and_seller_sees_it(self):
        resp = self.client.post(
            f"/api/listings/{self.listing.id}/offers/",
            {"amount": "5000", "message": "I can save this"},
            format="json",
            **self.auth(self.buyer),
        )
        self.assertEqual(resp.status_code, 201)
        # seller sees the offer on their listing
        resp = self.client.get(
            f"/api/listings/{self.listing.id}/offers/", **self.auth(self.seller)
        )
        self.assertEqual(resp.data["count"], 1)
        self.assertEqual(resp.data["results"][0]["buyer_username"], "buyer")

    def test_outsider_cannot_see_others_offers(self):
        self.client.post(
            f"/api/listings/{self.listing.id}/offers/",
            {"amount": "1", "message": ""},
            format="json",
            **self.auth(self.buyer),
        )
        outsider = User.objects.create_user("nosy")
        resp = self.client.get(
            f"/api/listings/{self.listing.id}/offers/", **self.auth(outsider)
        )
        self.assertEqual(resp.data["count"], 0)


class ExpiryTaskTests(TestCase):
    def test_expired_active_listings_flip_status(self):
        seller = User.objects.create_user("seller")
        old = Listing.objects.create(
            seller=seller,
            title="OldShip",
            category=make_category(),
            pitch="x",
            asset_types=["codebase"],
            pricing_mode="offer",
            expires_at=timezone.now() - timedelta(days=1),
        )
        fresh = Listing.objects.create(
            seller=seller,
            title="NewShip",
            category=make_category(),
            pitch="x",
            asset_types=["codebase"],
            pricing_mode="offer",
        )
        expire_listings()
        old.refresh_from_db()
        fresh.refresh_from_db()
        self.assertEqual(old.status, Listing.Status.EXPIRED)
        self.assertEqual(fresh.status, Listing.Status.ACTIVE)


class SavedSearchMatchingTests(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user("seller")
        self.category = make_category()
        self.listing = Listing.objects.create(
            seller=self.seller,
            title="MatchMe",
            category=self.category,
            pitch="x",
            asset_types=["codebase"],
            pricing_mode="fixed",
            price=Decimal("45000"),
            metrics={"mrr": 8000, "users": 3400},
            tech_stack=["python", "nextjs"],
        )

    def test_match_on_category_mrr_price(self):
        self.assertTrue(
            _matches(self.listing, {"category": "productivity", "min_mrr": 5000, "max_price": 50000})
        )

    def test_no_match_wrong_category(self):
        self.assertFalse(_matches(self.listing, {"category": "chatbots"}))

    def test_no_match_mrr_below_min(self):
        self.assertFalse(_matches(self.listing, {"min_mrr": 9000}))

    def test_no_match_price_above_max(self):
        self.assertFalse(_matches(self.listing, {"max_price": 10000}))

    def test_tech_stack_any_overlap(self):
        self.assertTrue(_matches(self.listing, {"tech_stack": ["rust", "python"]}))
        self.assertFalse(_matches(self.listing, {"tech_stack": ["rust", "go"]}))

    def test_empty_filters_match_everything(self):
        self.assertTrue(_matches(self.listing, {}))

    def test_savedsearch_task_skips_missing_listing(self):
        from .tasks import dispatch_savedsearch_alerts

        self.assertIsNone(dispatch_savedsearch_alerts(999999))
