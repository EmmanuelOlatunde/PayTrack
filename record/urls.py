from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Dashboard
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('add-payment/', views.add_payment, name='add_payment'),  # Add Payment
    path('monthly-records/', views.monthly_records, name='monthly_records'),  # Monthly Records
    path('edit-payment/<int:payment_id>/', views.edit_payment, name='edit_payment'),  # Edit Payment
]
