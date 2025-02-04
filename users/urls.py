from django.urls import path
from . import views


urlpatterns = [
    path('', views.authorization, name = 'authorization'),
    path('exit/', views.exit, name = 'exit'),
]