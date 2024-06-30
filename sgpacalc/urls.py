# FSD/sgpa/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('calculate/', views.calculate, name='calculate'),
    path('fetch_subjects/', views.fetch_subjects, name='fetch_subjects'),
    path('add/', views.add, name='add'),
    path('cgpa/', views.cgpa, name='cgpa'),
]
