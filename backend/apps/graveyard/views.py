from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .models import Grave, Reaction
from .serializers import GraveDetailSerializer, GraveListSerializer, SubmissionCreateSerializer


class GraveViewSet(viewsets.ReadOnlyModelViewSet):
    """G-01/G-02/US-1.2 — browse & search the graveyard.

    Query params: ?q= &status= &category= &cause= &year= &funding_min=
    """

    lookup_field = "slug"

    def get_queryset(self):
        qs = Grave.objects.select_related("category", "cause")
        params = self.request.query_params
        if q := params.get("q"):
            qs = qs.filter(Q(name__icontains=q) | Q(summary__icontains=q))
        if status := params.get("status"):
            qs = qs.filter(status=status)
        if category := params.get("category"):
            qs = qs.filter(category__slug=category)
        if cause := params.get("cause"):
            qs = qs.filter(cause__slug=cause)
        if year := params.get("year"):
            qs = qs.filter(died_on__year=year)
        if funding_min := params.get("funding_min"):
            qs = qs.filter(funding_raised__gte=funding_min)
        return qs

    def get_serializer_class(self):
        return GraveDetailSerializer if self.action == "retrieve" else GraveListSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]


class SubmissionCreateView(APIView):
    """US-2.1 — submit a death for moderation (throttled 5/day, BR-01 evidence)."""

    throttle_scope = "submission"
    permission_classes = [AllowAny]

    def get_throttles(self):
        return [ScopedRateThrottle()]

    def post(self, request):
        serializer = SubmissionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = serializer.save(submitter=request.user if request.user.is_authenticated else None)
        return Response(
            {"id": submission.id, "status": submission.status,
             "message": "Received. Moderated within 48h — you'll be credited on the tombstone."},
            status=201,
        )


class GraveDetailView(DetailView):
    """C3 tombstone page (SSR for SEO — P-03)."""

    template_name = "graveyard/grave_detail.html"
    context_object_name = "grave"
    model = Grave

    def get_queryset(self):
        return Grave.objects.select_related("category", "cause").prefetch_related("sources", "reactions", "comments")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grave = self.object
        context["sources"] = grave.sources.all()
        context["candle_count"] = grave.reactions.count()
        context["comments"] = grave.comments.select_related("user")
        context["mourned"] = (
            self.request.user.is_authenticated
            and Reaction.objects.filter(user=self.request.user, grave=grave).exists()
        )
        return context


def candle_view(request, slug):
    """US-1.5 — toggle the candle reaction (one per user per grave)."""
    if not request.user.is_authenticated:
        return redirect("grave-detail", slug=slug)
    grave = get_object_or_404(Grave, slug=slug)
    reaction = Reaction.objects.filter(user=request.user, grave=grave).first()
    if reaction:
        reaction.delete()
    else:
        Reaction.objects.create(user=request.user, grave=grave)
    return redirect("grave-detail", slug=slug)
