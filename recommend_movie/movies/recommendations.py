from django.db.models import Count

from .models import Favorite, Movie


def recommend_movies_for_user(user, limit=5):
    favorite_movie_ids = Favorite.objects.filter(user=user).values_list(
        'movie_id',
        flat=True,
    )

    similar_user_ids = (
        Favorite.objects.filter(movie_id__in=favorite_movie_ids)
        .exclude(user=user)
        .values_list('user_id', flat=True)
        .distinct()
    )

    return (
        Movie.objects.filter(favorites__user_id__in=similar_user_ids)
        .exclude(id__in=favorite_movie_ids)
        .annotate(recommend_score=Count('favorites'))
        .order_by('-recommend_score', '-created_at')[:limit]
    )
