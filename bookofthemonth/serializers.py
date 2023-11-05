from rest_framework import serializers
from .models import BookOfTheMonth


class BookOfTheMonthSerializer(serializers.ModelSerializer):

    def validate_image(self, value):
        if value.size > 2000 * 2000 * 2:
            raise serializers.ValidationError(
                'Image size exceeds 4 MB!'
            )
        if value.image.width > 1920:
            raise serializers.ValidationError(
                'Image width exceeds 1920px!'
            )
        if value.image.height > 1920:
            raise serializers.ValidationError(
                'Image height exceeds 1920px!'
            )
        return value

    class Meta:
        model = BookOfTheMonth
        fields = [
            'id', 'title', 'content', 'created_at',
            'updated_at', 'image'
        ]
