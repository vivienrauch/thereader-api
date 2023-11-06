from rest_framework import serializers
from .models import BookClubEvent
from responses.models import Response


class BookClubEventSerializer(serializers.ModelSerializer):
    """
    BookClubEvent serializer
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(sosurce='owner.profile.image.url')
    response_id = serializers.SerializerMethodField()
    response_count = serializers.ReadOnlyField()

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
    
    def get_response_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            response = Response.objects.filter(
                owner=user, bookclubevent=obj
            ).first()
            return response.id if response else None
        return None

    class Meta:
        model = BookClubEvent
        fields = [
            'id', 'owner', 'created_at', 'updated_at',
            'event_name', 'event_description',
        ]