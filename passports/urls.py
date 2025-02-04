from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name = 'index'),
    path('passport/<int:id>/', views.passport, name = 'passport'),
    path('passport_add/first/', views.passport_add_first, name = 'passport_add_first'),
    path('passport_add/second/<int:id>/', views.passport_add_second, name = 'passport_add_second'),
    path('passport_add/third/<int:id>/', views.passport_add_third, name = 'passport_add_third'),
    path('passport_add/forth/<int:id>/', views.passport_add_forth, name = 'passport_add_forth'),
    path('passport_add/fifth/<int:id>/', views.passport_add_fifth, name = 'passport_add_fifth'),
    path('passport_add/sixth/<int:id>/', views.passport_add_sixth, name = 'passport_add_sixth'),
    path('export/<int:id>/', views.export, name = 'export'),
]