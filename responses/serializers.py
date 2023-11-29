from django.db import IntegrityError
from rest_framework import serializers
from .models import Response


class ResponseSerializer(serializers.ModelSerializer):
    """
    Response serializer
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Response
        fields = [
            'id', 'owner', 'bookclubevent', 'created_at'
        ]

    """
    Checks for duplicate responses
    """
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })
