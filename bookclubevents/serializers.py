from rest_framework import serializers
from .models import BookClubEvent
from responses.models import Response
from datetime import time


class CustomizedTimeField(serializers.TimeField):
    def to_representation(self, value):
        if value is None:
            return None
        return value.strftime('%H:%M:%S')


class BookClubEventSerializer(serializers.ModelSerializer):
    """
    BookClubEvent serializer
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    response_id = serializers.SerializerMethodField()
    response_count = serializers.ReadOnlyField()
    event_start = CustomizedTimeField(default=time.min)
    event_end = CustomizedTimeField(default=time.min)

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
            'id', 'owner', 'created_at', 'updated_at', 'event_start',
            'event_end', 'event_cover', 'event_name', 'event_description',
            'is_owner', 'date', 'event_start',
            'event_end', 'event_location', 'event_organiser',
            'response_count', 'response_id', 'website',
            'contact', 'date',
        ]