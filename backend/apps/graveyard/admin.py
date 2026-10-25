from django.contrib import admin

from .models import CauseOfDeath, Category, Comment, Grave, Reaction, Source, Submission


class SourceInline(admin.TabularInline):
    model = Source
    extra = 1


@admin.register(Grave)
class GraveAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "category", "cause", "died_on", "funding_raised")
    list_filter = ("status", "category", "cause")
    search_fields = ("name", "summary")
    inlines = [SourceInline]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    """US-2.2 moderation queue: approve/reject with reason, 48h SLA (BR-05)."""

    list_display = ("id", "submitter", "status", "created_at", "moderator")
    list_filter = ("status",)
    readonly_fields = ("submitter", "payload", "created_at")
    actions = ["approve", "reject"]

    @admin.action(description="Approve selected submissions (mark for grave creation)")
    def approve(self, request, queryset):
        queryset.update(status="approved", moderator=request.user)

    @admin.action(description="Reject selected submissions")
    def reject(self, request, queryset):
        queryset.update(status="rejected", moderator=request.user)


admin.site.register(Category)
admin.site.register(CauseOfDeath)
admin.site.register(Reaction)
admin.site.register(Comment)
