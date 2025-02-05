from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),  # URL for the user list page
    path('chat/<int:receiver_id>/', views.chat_room, name='chat_room'),  # URL for the chat room
]