from rest_framework import serializers
from .models import Contact
from django.contrib.humanize.templatetags.humanize import naturaltime


class ContactSerializer(serializers.modelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    profile.id = serializers.ReadOnlyField(source="owner.profile.id")
    profile_image = serializers.ReadOnlyField(source="owner.profile.image.url")
    created_at = serializers.SerializerMethodField(method_name="get_humanized_created_at")
    updated_at = serializers.SerializerMethodField(method_name="get_humanized_updated_at")

    def get_humanized_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_humanized_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    class Meta:
        model = Contact
        fields = [
            "id",
            "owner",
            "reason",
            "content",
            "profile_id",
            "profile_image",
            "created_at",
            "updated_at",
        ]