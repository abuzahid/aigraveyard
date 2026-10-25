from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase

from .models import Category, CauseOfDeath, Grave, Reaction, Submission

User = get_user_model()


def make_grave(name="TestBot", status=Grave.Status.DEAD, **kwargs):
    category, _ = Category.objects.get_or_create(name="Chatbots", defaults={"slug": "chatbots"})
    cause, _ = CauseOfDeath.objects.get_or_create(name="Competition", defaults={"slug": "competition"})
    defaults = {
        "summary": "A test AI product",
        "status": status,
        "born_on": "2024-01-01",
        "category": category,
        "cause": cause,
    }
    defaults.update(kwargs)
    return Grave.objects.create(name=name, **defaults)


class GraveAPITests(APITestCase):
    def setUp(self):
        make_grave("DeadOne", died_on="2026-05-01")
        make_grave("DeadTwo", died_on="2025-05-01")
        make_grave("DelayedOne", status=Grave.Status.DELAYED)

    def test_list_is_paginated(self):
        resp = self.client.get("/api/graves/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("results", resp.data)
        self.assertIn("count", resp.data)

    def test_filter_by_status(self):
        resp = self.client.get("/api/graves/", {"status": "dead"})
        names = [g["name"] for g in resp.data["results"]]
        self.assertEqual(sorted(names), ["DeadOne", "DeadTwo"])

    def test_filter_by_year(self):
        resp = self.client.get("/api/graves/", {"status": "dead", "year": "2026"})
        self.assertEqual([g["name"] for g in resp.data["results"]], ["DeadOne"])

    def test_search_by_name(self):
        resp = self.client.get("/api/graves/", {"q": "delayedone"})
        self.assertEqual(resp.data["count"], 1)

    def test_detail_includes_candle_count(self):
        resp = self.client.get("/api/graves/deadone/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["candle_count"], 0)


class SubmissionTests(APITestCase):
    def test_evidence_link_required(self):
        resp = self.client.post(
            "/api/graves/submit/",
            {"name": "GhostAI", "category": "chatbots", "status": "dead"},
            format="json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_submission_created(self):
        resp = self.client.post(
            "/api/graves/submit/",
            {
                "name": "GhostAI",
                "category": "chatbots",
                "status": "dead",
                "shutdown_date": "2026-01-01",
                "evidence_link": "https://example.com/shutdown-notice",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Submission.objects.count(), 1)
        self.assertEqual(Submission.objects.first().status, "pending")


class TombstonePageTests(TestCase):
    def test_detail_page_renders(self):
        grave = make_grave("PageBot")
        resp = self.client.get(f"/graves/{grave.slug}/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "PageBot")

    def test_candle_toggle_requires_login(self):
        grave = make_grave("CandleBot")
        resp = self.client.post(f"/graves/{grave.slug}/candle/")
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Reaction.objects.count(), 0)

    def test_candle_toggle_once_per_user(self):
        user = User.objects.create_user("mourner")
        grave = make_grave("MournedBot")
        self.client.force_login(user)
        self.client.post(f"/graves/{grave.slug}/candle/")
        self.client.post(f"/graves/{grave.slug}/candle/")  # toggles off
        self.assertEqual(Reaction.objects.count(), 0)
