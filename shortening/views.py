from django.shortcuts import redirect, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from shortening.models import ShortUrl, ShortUrlRedirectInfo
from shortening.serializers import ShortUrlSerializer
from shortening.utils import get_client_ip, random_string


class ShortUrlListCreateView(generics.ListCreateAPIView):
    """List/Create for short url"""
    queryset = ShortUrl.objects.all()
    serializer_class = ShortUrlSerializer

    def get_queryset(self):
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )
        user_ip = get_client_ip(self.request)
        queryset = self.queryset.filter(created_by=user_ip)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(created_by=get_client_ip(request),
                        link_identifier=random_string(6))

        # return a response
        return Response(serializer.get_full_short_url, status=status.HTTP_201_CREATED)


class ShortUrlRetrieveDeleteView(generics.DestroyAPIView):
    """Retrieve/Delete for short url by id"""
    queryset = ShortUrl.objects.all()
    lookup_field = "id"
    serializer_class = ShortUrlSerializer

    def get(self, request, *args, **kwargs):
        short_url_id = self.kwargs["id"]
        user_ip = get_client_ip(request)

        obj = get_object_or_404(self.queryset, id=short_url_id, created_by=user_ip)
        serializer = self.get_serializer(data=request.data, instance=obj)

        return Response(serializer.get_full_short_url)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user_ip = get_client_ip(request)
        # check if user is author
        if instance.created_by != user_ip:
            return Response(status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShortUrlRedirect(generics.GenericAPIView):
    """Redirect from short to full url"""
    queryset = ShortUrl.objects.all()
    lookup_field = "link_identifier"

    def get(self, request, *args, **kwargs):
        short_url_obj = self.get_object()
        user_ip = get_client_ip(request)
        # create statistic object
        ShortUrlRedirectInfo(
            short_url=short_url_obj,
            clicked_by=user_ip).save()

        return redirect(short_url_obj.real_url)
