from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "get_roles", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        ("AI Graveyard", {"fields": ("roles", "notify_digest", "notify_watchlist", "notify_offers")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("AI Graveyard", {"fields": ("roles",)}),
    )

    @admin.display(description="Roles")
    def get_roles(self, obj):
        return ", ".join(obj.roles) or "—"
