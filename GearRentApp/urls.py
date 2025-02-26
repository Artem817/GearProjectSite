# GearRentApp/urls.py
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', include('django.contrib.auth.urls')),  # підключаємо стандартні маршрути для аутентифікації
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('logout/', views.logout_view, name='logout'),
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/add/', views.add_equipment, name='add_equipment'),
    path('equipment/edit/<int:pk>/', views.edit_equipment, name='edit_equipment'),
    path('equipment/delete/<int:pk>/', views.delete_equipment, name='delete_equipment'),
    path('clients/', views.client_list, name='client_list'),
    path('clients/add/', views.client_create, name='client_create'),
    path('clients/edit/<int:pk>/', views.client_edit, name='client_edit'),
    path('rentals/', views.rental_list, name='rental_list'),
    path('rentals/add/', views.rental_create, name='rental_create'),
    path('rentals/<int:pk>/', views.rental_detail, name='rental_detail'),
    path('clients/delete/<int:pk>/', views.client_delete, name='client_delete'),
    path('equipment/categories/', views.equipment_category_list, name='equipment_category_list'),
    path('equipment/categories/add/', views.equipment_category_create, name='equipment_category_create'),
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/add/', views.maintenance_create, name='maintenance_create'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/add/', views.reservation_create, name='reservation_create'),
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/add/', views.payment_create, name='payment_create'),
    path('rentals/<int:pk>/', views.rental_detail, name='rental_detail'),
    path('rentals/<int:pk>/complete/', views.rental_complete, name='rental_complete'),
]
