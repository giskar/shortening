from django.db import models


class ShortUrl(models.Model):
    id = models.AutoField(primary_key=True)
    real_url = models.TextField()
    url = models.CharField(max_length=6, unique=True)
    created_by = models.GenericIPAddressField()


class ShortUrlStatistic(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.ForeignKey(ShortUrl, on_delete=models.deletion.CASCADE)
    clicked_by = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
