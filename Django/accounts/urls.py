from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('user/', views.getUserInfo),
    path('<int:user_pk>/delete/', views.deleteUser),
    path('<int:user_pk>/user/', views.postUserInfo),
    path('<int:user_pk>/user/update/', views.updateUserInfo),
    path('<int:user_pk>/user/changePasswoed/', views.change_password),
    path('<int:user_pk>/follow/', views.follow),
]
