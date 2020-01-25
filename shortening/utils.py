import random
import string

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Max

from shortening.models import ShortUrl, ShortUrlStatistic


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def statistics_resp(**kwargs):
    return {
        "id": kwargs["id"],
        "url": kwargs["url"],
        "real_url": kwargs["real_url"],
        "last_click": kwargs.get("last_click", "never"),
        "click_count": kwargs.get("click_count", 0),
        "last_click_by": kwargs.get("last_click_by", None),
        }


def get_domain(request):
    return f"{request.scheme}://{request.META.get('HTTP_HOST', request.META['REMOTE_ADDR'])}/"


def get_full_short_url(request, short_url: ShortUrl):
    """Get full object for short link"""
    data = {
        "id": short_url.id,
        "url": f"{get_domain(request)}{short_url.url}",
        "real_url": short_url.real_url,
    }

    try:

        query = ShortUrlStatistic.objects \
            .filter(url=short_url) \
            .values("url").annotate(click_count=Count("url"),
                                    last_click=Max("timestamp"),
                                    ).get()

        data.update({
            "last_click": query["last_click"],
            "click_count": query["click_count"],
            "last_click_by": ShortUrlStatistic.objects.get(timestamp=query["last_click"]).clicked_by,
        })

    except ObjectDoesNotExist:
        pass

    return statistics_resp(**data)


def random_string(string_length):
    """Generate a random string with the combination of lowercase and uppercase letters """

    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(string_length))
