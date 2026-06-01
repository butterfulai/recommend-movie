from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Favorite, Movie
from .recommendations import recommend_movies_for_user


def home(request):
    popular_movies = (
        Movie.objects.annotate(favorite_count=Count('favorites'))
        .order_by('-favorite_count', '-created_at')[:8]
    )
    latest_movies = Movie.objects.order_by('-created_at')[:8]
    return render(
        request,
        'movies/home.html',
        {
            'popular_movies': popular_movies,
            'latest_movies': latest_movies,
        },
    )


@login_required
def mypage(request):
    recommendations = recommend_movies_for_user(request.user, limit=5)
    favorite_movies = Movie.objects.filter(favorites__user=request.user).order_by(
        '-favorites__created_at'
    )
    return render(
        request,
        'movies/mypage.html',
        {
            'recommendations': recommendations,
            'favorite_movies': favorite_movies,
        },
    )


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, movie=movie).exists()
    return render(
        request,
        'movies/detail.html',
        {
            'movie': movie,
            'is_favorite': is_favorite,
        },
    )


@login_required
@require_POST
def toggle_favorite(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, movie=movie)
    if not created:
        favorite.delete()
    return redirect('movie_detail', movie_id=movie.id)
