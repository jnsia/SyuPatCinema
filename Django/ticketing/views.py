from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from .models import *
from .serializers import *
from movies.serializers import *
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from django.http.response import JsonResponse


@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
def region_list(request):
    regions = Regions.objects.all()
    serializer = RegionListSerializer(regions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def theater_detail(request, region):
    theaters = Theater.objects.all()
    serializer = TheaterListSerailizer(theaters, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def theater_list(request):
    theaters = Theater.objects.all()
    serializer = TheaterListSerailizer(theaters, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def time_list(request, regions_pk, theater_pk, movie_pk):
    playdates = PlayDate.objects.filter(movie=movie_pk, theater=theater_pk)
    serializer = PlayDateListSerailizer(playdates, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def seat_list(request, regions_pk, theater_pk, movie_pk, time_pk):
    seats = Seat.objects.filter(time=time_pk)
    serializer = SeatSerailizer(seats, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def seat_push(request, time_pk, row, col):
    seat = Seat()
    time = PlayDate.objects.get(pk=time_pk)
    seat.time = time
    seat.row = row
    seat.col = col

    if Seat.objects.filter(time=time, row=row, col=col).exists():
        return JsonResponse({'msg': '이미 예약된 좌석입니다.'})

    seat.save()

    context = {
        'seat_id': seat.pk
    }

    return JsonResponse(context)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def reservation_list(request, user_pk):
    reservation = Reservation.objects.filter(user_id=user_pk)
    serializer = ReservationListSerializer(reservation, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def reservation_datail(request, user_pk):
    serializer = ReservationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def create_ticket(request, reservation_pk, theater_pk, movie_pk, time_pk, seat_pk):
    ticket = Ticket()
    
    reservation = Reservation.objects.get(pk=reservation_pk)
    theater = Theater.objects.get(pk=theater_pk)
    movie = Movie.objects.get(pk=movie_pk)
    time = PlayDate.objects.get(pk=time_pk)
    seat = Seat.objects.get(pk=seat_pk)

    ticket.reservation = reservation
    ticket.theater = theater
    ticket.movie = movie
    ticket.time = time
    ticket.seat = seat
    ticket.price = request.data['price']

    ticket.save()

    context = {
        'ticket_id': ticket.pk
    }

    return JsonResponse(context)
