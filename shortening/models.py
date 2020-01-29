from django.db import models


class ShortUrl(models.Model):
    id = models.AutoField(primary_key=True)
    real_url = models.URLField()
    link_identifier = models.CharField(max_length=6, unique=True)
    created_by = models.GenericIPAddressField()


class ShortUrlRedirectInfo(models.Model):
    id = models.AutoField(primary_key=True)
    short_url = models.ForeignKey(ShortUrl, on_delete=models.deletion.CASCADE)
    clicked_by = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)
