import requests
from django.conf import settings
from models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view

api_key_value = settings.API_KEY_VALUE
BASE_URL = 'https://api.themoviedb.org/3'
IMAGE_URL = 'https://image.tmdb.org/t/p/w500'

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_key_value}"
}

@api_view(['GET'])
def getGenre(request):
    url = f"{BASE_URL}/genre/movie/list?language=ko-kR"

    response = requests.get(url, headers=headers).json()
    print(response)
    
    genres = response['genres']
    genre_list = Genre.objects.all()
    
    genre_id_list = []
    
    for genre_set in genre_list:
        genre_id_list.append(genre_set.genre_id)
        
    print(genres)
    
    for genre in genres:
        if genre['id'] not in genre_id_list:
            genreData = Genre(genre_id=genre['id'], name=genre['name'])
            genreData.save()
                
    return Response(response)


@api_view(['GET'])
def now_playing_movies(request):
    for page in range(1, 5):
        url = f"{BASE_URL}/movie/now_playing?language=ko-KR&page={page}"
        
        response = requests.get(url, headers=headers).json()
        results = response['results']
        
        movie_list = Movie.objects.all()
        movie_id_list = []

        for movie_set in movie_list:
            movie_id_list.append(movie_set.movie_id)   
            # movie_set.delete()
        
        for result in results:
            if not result['overview']:
                continue
            
            if result['id'] in movie_id_list:
                continue
            
            movieData = Movie()
            
            url = f"{BASE_URL}/movie/{result['id']}?language=ko-KR"
            response = requests.get(url, headers=headers).json()
            
            movieData.movie_id = result['id']
            movieData.title = result['title']
            movieData.description = result['overview']
            movieData.backdrop_path = IMAGE_URL + result['backdrop_path']
            movieData.poster_path = IMAGE_URL + result['poster_path']
            movieData.popularity = result['popularity']
            movieData.runtime = response['runtime']
            
            movieData.save()
        
            for genre in result['genre_ids']:
                genreData = Genre.objects.get(genre_id=genre)
                movieData.genres.add(genreData.pk)

    return Response(results)