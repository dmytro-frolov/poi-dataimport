from statistics import mean

from django.contrib import admin

from point_of_interest.models import Category, Location, Poi


@admin.register(Poi)
class PoiAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "external_id",
        "name",
        "location",
        "description",
        "provider",
        "category",
        "average_rating",
        "created_at",
    )
    search_fields = ("name", "description", "category__name", "provider")
    list_filter = ("provider", "category")

    @admin.display(description="Average Rating")
    def average_rating(self, obj):
        return mean(obj.ratings)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("zip", "address", "latitude", "longitude")
    search_fields = ("zip", "address")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
