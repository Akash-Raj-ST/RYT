from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('register', views.register),
    path('home',views.all_place_cat),
    path('profile',views.profile),
    path('places/<place_id>', views.places),
    path('review', views.review),
    path('like/<r_id>',views.like),
    path('logout', views.logout),
]