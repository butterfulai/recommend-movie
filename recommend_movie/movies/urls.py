from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mypage/', views.mypage, name='mypage'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path(
        'movies/<int:movie_id>/favorite/',
        views.toggle_favorite,
        name='toggle_favorite',
    ),
]
