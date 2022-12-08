from django.contrib import admin

from .models import Advertisement, FavoritesAdvertisements


@admin.register(Advertisement)
class AdminAdvertisement(admin.ModelAdmin):
    list_display = ['id', 'creator', 'status', 'title', 'created_at', 'updated_at', 'draft']
    list_editable = ['creator', 'status', 'title', 'draft']

@admin.register(FavoritesAdvertisements)
class AdminFavoritesAdvertisements(admin.ModelAdmin):
    list_display = ['id', 'user']