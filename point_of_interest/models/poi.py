from django.contrib.postgres.fields import ArrayField
from django.db import models


class Poi(models.Model):
    external_id = models.CharField(max_length=256, null=False)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512)
    ratings = ArrayField(models.IntegerField(), blank=True)
    provider = models.CharField(max_length=64)

    location = models.ForeignKey("Location", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
