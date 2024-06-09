from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("chat/<str:room_namee>/", views.room, name="room"),
]