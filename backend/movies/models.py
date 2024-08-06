from django.db import models
from django.conf import settings


class Genre(models.Model):
    genre_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_like_genres')


class Movie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    movie_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    backdrop_path = models.TextField()
    poster_path = models.TextField()
    popularity = models.FloatField()
    runtime = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name='movies')


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_write_reviews")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_like_review')
    content = models.CharField(max_length=200)
    score = models.FloatField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
