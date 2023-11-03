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