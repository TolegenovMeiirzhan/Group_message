from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('create-room/', createRoom, name='create-room'),
    path('update-room/<str:pk>/', updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', deleteRoom, name='delete-room'),
    path('delete-message/<str:pk>/', deleteMessage, name='delete-message'),
    path('update-message/<str:pk>/', updateMessage, name='update-message'),
    path('room/<str:pk>/', getRoom, name='room'),
    path('user/<str:pk>/', getUser, name='user'),
    path('topic/<str:pk>/', getTopic, name='topic'),
    path('login/', loginUser, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('register/', registerUser, name='register'),
    # path('join/<str:pk>/', getJoin, name='join'),
]