from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.login),
    path('register', views.register),
    path('home',views.home),
    path('places/<int:p_id>',views.place),
]
