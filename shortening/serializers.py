from rest_framework import serializers

from shortening.models import ShortUrl


class ShortUrlSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    real_url = serializers.URLField(required=True)
    url = serializers.CharField(read_only=True)
    created_by = serializers.CharField(read_only=True)

    class Meta:
        model = ShortUrl
        fields = ['id', 'real_url', 'url', 'created_by']
