from django.urls import path
from . import views

urlpatterns = [
    path('Login/', views.LoginPage, name="login"),
    path('Logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('room/<int:pk>/', views.room, name="room"),

    path('create-room/', views.CreateRoom, name="create-room"),
    path('update-room/<int:pk>/', views.UpdateRoom, name="update-room"),
    path('delete-room/<int:pk>/', views.deleteRoom, name="delete-room"),
]
