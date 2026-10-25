from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Role

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Public sign-up (US-5.1). Roles are multi-selectable."""

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True, default="")
    password = serializers.CharField(write_only=True, min_length=8, style={"input_type": "password"})
    roles = serializers.ListField(
        child=serializers.ChoiceField(choices=Role.choices),
        default=list,
        required=False,
    )

    class Meta:
        model = User
        fields = ("username", "email", "password", "roles")

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def create(self, validated_data):
        roles = validated_data.pop("roles", []) or ["reader"]
        if not roles:
            roles = ["reader"]
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        user.roles = roles
        user.save(update_fields=["roles"])
        return user
