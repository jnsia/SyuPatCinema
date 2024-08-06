from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list),
    path('<int:movie_pk>/', views.movie_detail),
    path('genre/<str:genre_name>/', views.genre_movie_list),
    path('genres/', views.genre_list),
    path('<int:movie_pk>/reviews/', views.review_list),
    path('<int:movie_pk>/reviews/create/', views.review_create),
    path('<int:movie_pk>/reviews/<int:review_pk>/', views.review_detail),
    path('<int:movie_pk>/reviews/<int:review_pk>/likes/', views.like_review),
    # path('now_playing/', views.now_playing_movies),
    # path('get_genre/', views.getGenre),
]
