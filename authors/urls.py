from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('keepawake/', views.keepawake)
]