from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import get_user_model
from allauth.account.adapter import get_adapter
from movies.serializers import ReviewSerializer, GenreSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"


class UserDetailsSerializer(serializers.ModelSerializer):
    # followers = UserSerializer(many=True, read_only=True)
    # followings = UserSerializer(many=True, read_only=True)
    user_write_reviews = ReviewSerializer(many=True, read_only=True)
    user_like_genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "pk",
            "username",
            "email",
            "name",
            "birth",
            "phoneNumber",
            "followers",
            "followings",
            "user_write_reviews",
            "user_like_genres",
            "photo",
        )
        read_only_fields = (
            "user_write_reviews",
            "user_like_genres",
            "followers",
            "followings",
            "photo",
        )


class CustomRegisterSerializer(RegisterSerializer):
    genres = [
        [1, "액션"],
        [2, "모험"],
        [3, "애니메이션"],
        [4, "코미디"],
        [5, "범죄"],
        [6, "다큐멘터리"],
        [7, "드라마"],
        [8, "가족"],
        [9, "판타지"],
        [10, "역사"],
        [11, "공포"],
        [12, "음악"],
        [13, "미스터리"],
        [14, "로맨스"],
        [15, "SF"],
        [16, "TV 영화"],
        [17, "스릴러"],
        [18, "전쟁"],
        [19, "서부"],
    ]

    choice_list = [genre for genre in genres]

    name = serializers.CharField()
    birth = serializers.DateField()
    phoneNumber = PhoneNumberField(region="KR")
    like_genres = serializers.MultipleChoiceField(choices=choice_list)
    photo = serializers.ImageField(required=False)

    def get_cleaned_data(self):
        return {
            "username": self.validated_data.get("username", ""),
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
            "name": self.validated_data.get("name", ""),
            "birth": self.validated_data.get("birth", ""),
            "phoneNumber": self.validated_data.get("phoneNumber", ""),
            "like_genres": self.validated_data.get("like_genres", []),
            "photo": self.validated_data.get("photo", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        return user
