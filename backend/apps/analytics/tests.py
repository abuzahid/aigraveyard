from django.core.cache import cache
from rest_framework.test import APITestCase

from apps.graveyard.models import Grave
from apps.graveyard.tests import make_grave


class StatsTests(APITestCase):
    def setUp(self):
        cache.clear()  # stats endpoint caches for 5 min — don't leak between tests

    def test_stats_exclude_unconfirmed_and_total_capital(self):
        make_grave("FundedDead", funding_raised="1000000")
        make_grave("UnconfirmedOne", status=Grave.Status.UNCONFIRMED)

        resp = self.client.get("/api/stats/")
        self.assertEqual(resp.status_code, 200)
        # only the confirmed dead grave counts; unconfirmed is excluded entirely
        self.assertEqual(resp.data["totals"]["graves"], 1)
        self.assertEqual(resp.data["totals"]["documented"], 1)
        self.assertEqual(float(resp.data["totals"]["capital_buried"]), 1000000.0)
