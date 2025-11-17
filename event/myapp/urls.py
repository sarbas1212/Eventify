from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    path('services/', views.services, name='services'),
    path('service/<int:service_id>/types/', views.service_types, name='service_types'),
    path('service/<int:service_id>/type/<int:type_id>/', views.service_detail, name='service_detail'),


    path('contact/', views.contact, name='contact'),

    path('book/', views.book, name='book'),
    path('booking_view', views.booking_view, name='booking_view'),
    path('booking/<int:pk>/', views.booking_detail, name='booking_detail'),

    # path('book/<int:type_id>/', views.book, name='book'),
]
