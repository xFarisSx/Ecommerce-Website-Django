from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('stripe', views.stripe_transaction, name="checkout.stripe"),
    path('paypal', views.paypal_transaction, name="checkout.paypal"),
    path('stripe/config', views.stripe_config, name='checkout.stripe.config')
]
