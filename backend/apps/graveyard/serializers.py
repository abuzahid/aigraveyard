from rest_framework import serializers

from .models import CauseOfDeath, Category, Comment, Grave, Source, Submission


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ("url", "title", "published_on")


class GraveListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="slug", read_only=True)
    cause = serializers.SlugRelatedField(slug_field="slug", read_only=True)

    class Meta:
        model = Grave
        fields = (
            "id", "name", "slug", "summary", "status", "born_on", "died_on",
            "funding_raised", "region", "category", "cause",
        )


class GraveDetailSerializer(GraveListSerializer):
    sources = SourceSerializer(many=True, read_only=True)
    candle_count = serializers.SerializerMethodField()

    class Meta(GraveListSerializer.Meta):
        fields = GraveListSerializer.Meta.fields + ("narrative", "sources", "candle_count", "created_at")

    def get_candle_count(self, obj) -> int:
        return obj.reactions.count()


class SubmissionCreateSerializer(serializers.Serializer):
    """US-2.1 — C7 'Report a Death' form. Evidence link is mandatory (BR-01)."""

    name = serializers.CharField(max_length=200)
    url = serializers.URLField(required=False, allow_blank=True)
    category = serializers.CharField(max_length=100)
    status = serializers.ChoiceField(choices=Grave.Status.choices, default=Grave.Status.DEAD)
    shutdown_date = serializers.DateField(required=False, allow_null=True)
    evidence_link = serializers.URLField()
    context = serializers.CharField(required=False, allow_blank=True, max_length=2000)

    def save(self, **kwargs):
        submitter = kwargs["submitter"]
        payload = dict(self.validated_data)
        if payload.get("shutdown_date"):
            payload["shutdown_date"] = str(payload["shutdown_date"])  # JSON-safe
        return Submission.objects.create(submitter=submitter, payload=payload)


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "username", "body", "created_at")
