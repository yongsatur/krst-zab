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

    path('passport_update/first/<int:id>/', views.passport_update_first, name = 'passport_update_first'),
    path('passport_update/third/<int:id>/', views.passport_update_third, name = 'passport_update_third'),
    path('passport_update/forth/<int:id>/', views.passport_update_forth, name = 'passport_update_forth'),

    path('passport_delete/second/<int:id>/', views.passport_delete_second, name = 'passport_delete_second'),
    path('passport_delete/fifth/<int:id>/', views.passport_delete_fifth, name = 'passport_delete_fifth'),
    path('passport_delete/sixth/<int:id>/', views.passport_delete_sixth, name = 'passport_delete_sixth'),

    path('export/<int:id>/', views.export, name = 'export'),
]