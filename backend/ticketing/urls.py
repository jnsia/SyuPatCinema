from django.urls import path
from . import views

# mypjt/urls.py
# path('ticketing/', include('ticketing.urls')),
urlpatterns = [
    path('regions/', views.region_list),
    path('theaters/', views.theater_list),
    path('movies/', views.movie_list),
    path('<int:regions_pk>/<int:theater_pk>/<int:movie_pk>/times/', views.time_list),
    path('<int:regions_pk>/<int:theater_pk>/<int:movie_pk>/<int:time_pk>/seat/', views.seat_list),
    path('<int:time_pk>/<row>/<col>/seat/', views.seat_push),
    path('reservation/<int:user_pk>/', views.reservation_list),
    path('reservation/<int:user_pk>/detail/', views.reservation_datail),
    path('create_ticket/<int:reservation_pk>/<int:theater_pk>/<int:movie_pk>/<int:time_pk>/<int:seat_pk>/', views.create_ticket)
    # path('theaterDataSetting/', views.theaterDataSetting),
    # path('datatimeDataSetting/', views.datatimeDataSetting)
]
