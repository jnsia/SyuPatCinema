from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import get_user_model
from allauth.account.adapter import get_adapter
# from movies.serializers import ReviewSerializer
from movies.serializers import ReviewSerializer, GenreSerializer
from movies.models import Genre

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'

class UserDetailsSerializer(serializers.ModelSerializer):
    # followers = UserSerializer(many=True, read_only=True)
    # followings = UserSerializer(many=True, read_only=True)
    user_write_reviews = ReviewSerializer(many=True, read_only=True)
    like_genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('pk', 'username', 'email', 'name', 'birth', 'phoneNumber', 'followers', 'followings', 'user_write_reviews', 'like_genres', 'photo')
        read_only_fields = ('user_write_reviews', 'like_genres', 'followers', 'followings', 'photo', )

class CustomRegisterSerializer(RegisterSerializer):
    choice_list = [[genre.pk, genre.name] for genre in Genre.objects.all()]

    name = serializers.CharField()
    birth = serializers.DateField()
    phoneNumber = PhoneNumberField(region="KR")
    like_genres = serializers.MultipleChoiceField(choices=choice_list)
    photo = serializers.ImageField(required=False)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'name': self.validated_data.get('name', ''),
            'birth': self.validated_data.get('birth', ''),
            'phoneNumber': self.validated_data.get('phoneNumber', ''),
            'like_genres': self.validated_data.get('like_genres', []),
            'photo': self.validated_data.get('photo', ''),
        }
        
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        return user