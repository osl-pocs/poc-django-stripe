from django.urls import path

from . import views

app_name = "poc_django_stripe.payments"

urlpatterns = [
    path("", views.MainPageView.as_view(), name="main"),
    path("config/", views.stripe_config),
    path(
        "subscription/",
        views.SubscriptionPageView.as_view(),
        name="subscription",
    ),
    path(
        "stripe/subscription/<str:product_id>/<str:price_id>",
        views.stripe_subscription,
        name="stripe-subscription",
    ),
    path(
        "subscription/success/",
        views.SubscriptionSuccessPageView.as_view(),
        name="subscription-success",
    ),
    path(
        "subscription/cancelled/",
        views.SubscriptionCancelledPageView.as_view(),
        name="subscription-cancelled",
    ),
    path(
        "subscription/<str:subscription_id>/cancel",
        views.SubscriptionCancelView.as_view(),
        name="subscription-cancel",
    ),
    path(
        "subscription/<str:subscription_id>/reactivate",
        views.SubscriptionReactivateView.as_view(),
        name="subscription-reactivate",
    ),
    # path("webhook/", views.stripe_webhook),
    path(
        "customer-portal/",
        views.CustomerPortalPageView.as_view(),
        name="customer-portal",
    ),
    path(
        "stripe/customer-portal/",
        views.stripe_customer_portal,
        name="stripe-customer-portal",
    ),
]
