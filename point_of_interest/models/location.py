from django.db import models


class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    zip = models.CharField()
    address = models.CharField()

    def __str__(self):
        return f"Latitude: {self.latitude}, Longitude: {self.longitude}"
