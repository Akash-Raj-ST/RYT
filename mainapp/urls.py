from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.login,name="login"),
    path('register', views.register),
    path('home',views.home),
    path('profile/<int:user_id>',views.profile,name="profile"),
    path('places/<int:p_id>/',views.place,name="place"),
    path('places/<int:p_id>/add_review',views.add_review),
]
