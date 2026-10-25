from django.core.cache import cache
from django.db.models import Count, F, Sum
from django.db.models.functions import TruncQuarter
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.graveyard.models import Grave


class StatsView(APIView):
    """G-06/C8 — the shareable stats dashboard (P-06 embed widget source).
    Cached 5 minutes. Unconfirmed entries excluded (US-2.3)."""

    def get(self, request):
        data = cache.get("graveyard_stats")
        if data is None:
            graves = Grave.objects.exclude(status=Grave.Status.UNCONFIRMED)
            dead = graves.filter(status=Grave.Status.DEAD)

            per_quarter = (
                dead.filter(died_on__isnull=False)
                .annotate(quarter=TruncQuarter("died_on"))
                .values("quarter")
                .annotate(deaths=Count("id"))
                .order_by("quarter")
            )
            top_causes = (
                graves.filter(cause__isnull=False)
                .values("cause__name", "cause__slug")
                .annotate(deaths=Count("id"))
                .order_by("-deaths")[:8]
            )
            biggest = dead.filter(funding_raised__isnull=False).order_by("-funding_raised")[:10]

            data = {
                "totals": {
                    "graves": dead.count(),
                    "capital_buried": dead.aggregate(t=Sum("funding_raised"))["t"] or 0,
                    "documented": graves.count(),
                },
                "deaths_per_quarter": [
                    {
                        "quarter": f"{row['quarter'].year}-Q{(row['quarter'].month - 1) // 3 + 1}",
                        "deaths": row["deaths"],
                    }
                    for row in per_quarter
                ],
                "top_causes": [
                    {"name": row["cause__name"], "slug": row["cause__slug"], "deaths": row["deaths"]}
                    for row in top_causes
                ],
                "biggest_graves": [
                    {"name": g.name, "slug": g.slug, "funding_raised": str(g.funding_raised)}
                    for g in biggest
                ],
            }
            cache.set("graveyard_stats", data, 300)
        return Response(data)
