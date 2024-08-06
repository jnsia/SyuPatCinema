from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from movies.serializers import *


class SeatSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ('id', 'row', 'col', )
        read_only_fields = ('time', )


class PlayDateListSerailizer(serializers.ModelSerializer):
    class Meta:
        model = PlayDate
        fields = ('id', 'date', 'time', )


class TheaterListSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Theater
        fields = ('id','regions', 'name',)


class TicketListSerializer(serializers.ModelSerializer):
    class MovieListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('id', 'title', 'poster_path', 'runtime', 'genres', )

    movie = MovieListSerializer(read_only=True)
    theater = TheaterListSerailizer(read_only=True)
    seat = SeatSerailizer(read_only=True)
    time = PlayDateListSerailizer(read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'


class RegionListSerializer(serializers.ModelSerializer):
    theater_set = TheaterListSerailizer(many=True, read_only=True)
    
    class Meta:
        model = Regions
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ('user', )

class ReservationListSerializer(serializers.ModelSerializer):
    ticket_set = TicketListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Reservation
        fields = '__all__'