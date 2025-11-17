from django.urls import path
from . import views

app_name = "payment"  # <-- This line registers the namespace!

urlpatterns = [
    path('review/', views.payment_review, name='payment_review'),      # For estimate/confirmation/payment step
    path('finalize/', views.payment_finalize, name='payment_finalize'), # Save booking, finalize payment

    path('success/', views.payment_success, name='payment_success'),
    # path('failure/', views.payment_failure, name='payment_failure'),

    # path('', views.payment, name='payment'),  # You can keep this as the default endpoint if needed
]
