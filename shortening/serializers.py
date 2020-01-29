from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Max
from rest_framework import serializers
from shortening.utils import get_domain

from shortening.models import ShortUrl, ShortUrlRedirectInfo


class ShortUrlSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    real_url = serializers.URLField(required=True)
    link_identifier = serializers.CharField(read_only=True)
    created_by = serializers.CharField(read_only=True)

    class Meta:
        model = ShortUrl
        fields = ['id', 'real_url', 'link_identifier', 'created_by']

    @property
    def get_full_short_url(self):
        """Get full object for short link"""
        short_url = self.instance
        request = self._context["request"]

        data = {
            "id": short_url.id,
            "url": f"{get_domain(request)}{short_url.link_identifier}",
            "real_url": short_url.real_url,
        }

        try:

            query = ShortUrlRedirectInfo.objects \
                .filter(short_url=short_url) \
                .values("short_url").annotate(click_count=Count("id"),
                                              last_click=Max("created_at"),
                                              ).get()
            last_click_by = ShortUrlRedirectInfo.objects.filter(created_at=query["last_click"],
                                                                short_url=short_url).order_by('-created_at')\
                .first().clicked_by

            data.update({
                "last_click": query["last_click"],
                "click_count": query["click_count"],
                "last_click_by": last_click_by,
            })

        except ObjectDoesNotExist:
            pass

        return {
            "id": data["id"],
            "url": data["url"],
            "real_url": data["real_url"],
            "last_click": data.get("last_click", "never"),
            "click_count": data.get("click_count", 0),
            "last_click_by": data.get("last_click_by", None),
            }
