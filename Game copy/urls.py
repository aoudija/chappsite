from django.contrib import admin
from django.urls import path, include
from .views import matchView

urlpatterns = [
    path('<str:player>/<str:opponent>/', matchView.as_view()),
]
