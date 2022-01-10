from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="index"),
    path('', views.vod_del, name="vod_del"),
]
