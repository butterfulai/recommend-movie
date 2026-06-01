from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Favorite, Movie
from .recommendations import recommend_movies_for_user


class RecommendationTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username='main',
            email='main@example.com',
            password='pass',
        )
        self.similar_user = user_model.objects.create_user(
            username='similar',
            email='similar@example.com',
            password='pass',
        )
        self.other_user = user_model.objects.create_user(
            username='other',
            email='other@example.com',
            password='pass',
        )
        self.shared_movie = Movie.objects.create(
            title='Shared',
            genre='SF',
            description='A shared favorite.',
        )
        self.recommended_movie = Movie.objects.create(
            title='Recommended',
            genre='Action',
            description='Liked by a similar user.',
        )
        self.unrelated_movie = Movie.objects.create(
            title='Unrelated',
            genre='Drama',
            description='Liked by someone unrelated.',
        )
        Favorite.objects.create(user=self.user, movie=self.shared_movie)
        Favorite.objects.create(user=self.similar_user, movie=self.shared_movie)
        Favorite.objects.create(user=self.similar_user, movie=self.recommended_movie)
        Favorite.objects.create(user=self.other_user, movie=self.unrelated_movie)

    def test_recommends_movies_liked_by_similar_users(self):
        recommendations = list(recommend_movies_for_user(self.user))

        self.assertEqual(recommendations, [self.recommended_movie])

    def test_favorite_is_unique_per_user_and_movie(self):
        with self.assertRaises(Exception):
            Favorite.objects.create(user=self.user, movie=self.shared_movie)


class MovieViewTests(TestCase):
    def test_home_page_is_public(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)


class EmailAccountTests(TestCase):
    def test_user_can_signup_with_email_and_password_only(self):
        response = self.client.post(
            reverse('account_signup'),
            {
                'email': 'new@example.com',
                'password1': 'StrongPassword123',
                'password2': 'StrongPassword123',
            },
        )

        self.assertRedirects(response, reverse('mypage'))
        self.assertTrue(
            get_user_model().objects.filter(email='new@example.com').exists()
        )

    def test_email_address_must_be_unique(self):
        get_user_model().objects.create_user(
            username='existing',
            email='duplicate@example.com',
            password='StrongPassword123',
        )

        response = self.client.post(
            reverse('account_signup'),
            {
                'email': 'duplicate@example.com',
                'password1': 'StrongPassword123',
                'password2': 'StrongPassword123',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            get_user_model().objects.filter(email='duplicate@example.com').count(),
            1,
        )

    def test_user_can_login_with_email_and_password(self):
        get_user_model().objects.create_user(
            username='login-user',
            email='login@example.com',
            password='StrongPassword123',
        )

        response = self.client.post(
            reverse('account_login'),
            {
                'login': 'login@example.com',
                'password': 'StrongPassword123',
            },
        )

        self.assertRedirects(response, reverse('mypage'))
