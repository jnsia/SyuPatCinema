from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from allauth.account.adapter import DefaultAccountAdapter
from movies.models import Genre
from PIL import Image


class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    photo = models.ImageField(blank=True, default='profile/defaultProfile.jpeg', upload_to='profile/')
    name = models.CharField(max_length=15)
    birth = models.DateField(auto_now=False, null=True, blank=True)
    phoneNumber = PhoneNumberField()
    
    
class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_email, user_field, user_username

        data = form.cleaned_data
        
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        username = data.get("username")
        name = data.get("name")
        birth = data.get("birth")
        phoneNumber = data.get("phoneNumber")
        genres = request.data.getlist("like_genres[]")
        photo = request.FILES.get('photo')

        user_email(user, email)
        user_username(user, username)

        if name:
            user.name = name
        
        if birth:
            user.birth = birth
            
        if phoneNumber:
            user.phoneNumber = phoneNumber
        
        if first_name:
            user_field(user, "first_name", first_name)

        if last_name:
            user_field(user, "last_name", last_name)

        if photo:
            img_path = f'profile_{username}.png'
            img = Image.open(photo)
            img.save(f'media/profile/{img_path}','png')
            user_field(user, "photo", f'profile/{img_path}')

        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        
        self.populate_username(request, user)

        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()

        for genre_id in genres:
            user.like_genres.add(genre_id)

        return user
