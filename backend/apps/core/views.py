from django.shortcuts import render

from apps.graveyard.models import Grave
from apps.lifeboat.models import Listing


def home_view(request):
    """C1 Home page: dual 'RIP This Month' + 'Sinking Ships' feeds + counters."""
    recent_graves = (
        Grave.objects.filter(status=Grave.Status.DEAD, died_on__isnull=False)
        .select_related("category", "cause")
        .order_by("-died_on")[:10]
    )
    sinking = (
        Listing.objects.filter(status=Listing.Status.ACTIVE)
        .select_related("category")[:6]
    )
    context = {
        "recent_graves": recent_graves,
        "sinking": sinking,
        "grave_count": Grave.objects.filter(status=Grave.Status.DEAD).count(),
        "sinking_count": Listing.objects.filter(status=Listing.Status.ACTIVE).count(),
    }
    return render(request, "home.html", context)
