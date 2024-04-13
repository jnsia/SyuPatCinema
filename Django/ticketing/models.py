from django.db import models
from django.conf import settings
from movies.models import *

class Regions(models.Model):
    name = models.CharField(max_length=20)

class Theater(models.Model):
    regions = models.ForeignKey(Regions, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie)
    name = models.CharField(max_length=20)

class PlayDate(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.TextField()
    time = models.TextField()

class Seat(models.Model):
    time = models.ForeignKey(PlayDate, on_delete=models.CASCADE)
    row = models.CharField(max_length=5)
    col = models.CharField(max_length=5)

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Ticket(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.PROTECT)
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT)
    time = models.ForeignKey(PlayDate, on_delete=models.PROTECT)
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT)
    price = models.IntegerField()

