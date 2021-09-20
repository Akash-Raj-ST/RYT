from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('register', views.register),
    path('home',views.all_place_cat),
    path('places/<place_id>', views.places),
    path('review', views.review),
    path('logout', views.logout),
]