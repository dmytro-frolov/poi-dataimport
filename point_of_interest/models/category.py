from django.db import models


class Category(models.Model):
    name = models.CharField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
