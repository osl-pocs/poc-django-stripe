from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("", views.CheckoutPageView.as_view(), name="main"),
    path("config/", views.stripe_config),
    path("checkout-success/", views.CheckoutSuccessPageView.as_view()),
    path("checkout-cancelled/", views.CheckoutCancelledPageView.as_view()),
    path("webhook/", views.stripe_webhook),
    path(
        "customer-portal/",
        views.CustomerPortalPageView.as_view(),
        name="customer-portal",
    ),
    path(
        "stripe-checkout/",
        views.stripe_checkout_session,
        name="stripe-checkout",
    ),
    path(
        "stripe-customer-portal/",
        views.stripe_customer_portal,
        name="stripe-customer-portal",
    ),
]
