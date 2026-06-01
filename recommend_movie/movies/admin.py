from django.contrib import admin
from .models import Favorite, Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'created_at')
    search_fields = ('title', 'genre', 'description')
    list_filter = ('genre',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'created_at')
    search_fields = ('user__username', 'user__email', 'movie__title')
    list_filter = ('created_at',)
