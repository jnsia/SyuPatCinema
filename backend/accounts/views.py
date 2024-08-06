from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserDetailsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from .models import User
from rest_framework import status
from django.contrib.auth.hashers import check_password
from PIL import Image


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def getUserInfo(request):
    serializer = UserDetailsSerializer(request.user)
    return Response(serializer.data)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
def deleteUser(request, user_pk):
    person = User.objects.get(id=user_pk)
    person.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def getOhterUserInfo(request, user_pk):
    person = User.objects.get(id=user_pk)
    serializer = UserDetailsSerializer(person)
    return Response(serializer.data)
        

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
def updateUserInfo(request, user_pk):
    person = User.objects.get(pk=user_pk)

    if person != request.user:
        return Response({'msg': '접근불가'})
    
    username = request.data.get('username')
    photo = request.data.get('photo')

    serializer = UserDetailsSerializer(instance=person, data=request.data)
    selected_genres = request.data.getlist('like_genres[]')

    if serializer.is_valid(raise_exception=True):
        user = serializer.save()

        if photo:
            img_path = f'profile_{username}.png'
            img = Image.open(photo)
            img.save(f'media/profile/{img_path}','png')
            user.photo = f'/profile/{img_path}'

        user.save()

        like_genre_list = [like_genre.id for like_genre in person.like_genres.all()]

        for genre in selected_genres:
            person.like_genres.add(genre)

        for like_genre in like_genre_list:
            if str(like_genre) not in selected_genres:
                person.like_genres.remove(like_genre)

        return Response(serializer.data)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request, user_pk):
    person = User.objects.get(pk=user_pk)
    password = request.data['password']

    if check_password(password, person.password):
        password1 = request.data['password1']
        password2 = request.data['password2']

        if password1 == password2:
            person.set_password(password1)
            person.save()
            return Response(status=status.HTTP_200_OK)
        return Response({'msg': '새로운 비밀번호를 다시 확인해주세요'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'msg': '현재 비밀번호가 일치하지 않음'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def follow(request, user_pk):
    User = get_user_model()
    person = User.objects.get(pk=user_pk)
    if person != request.user:
        if person.followers.filter(pk=request.user.pk).exists():
            person.followers.remove(request.user.pk)
            print(person.followers)
            is_followed = False
        else:
            person.followers.add(request.user.pk)
            print(person.followers)
            is_followed = True
        context = {
            'is_followed': is_followed,
        }
        return JsonResponse(context)
