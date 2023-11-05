from rest_framework import serializers
from .models import BookClubEvent


class BookClubEventSerializer(serializers.ModelSerializer):
    """
    BookClubEvent serializer
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(sosurce='owner.profile.image.url')

    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size exceeds 2MB!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width exceeds 4096px!'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height exceeds 4096px!'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner
    