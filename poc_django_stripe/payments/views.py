import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView
from djstripe import webhooks
from djstripe.models import Customer, Product  # , Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY


def _get_payments_url(request, view_name="payments:main"):
    return request.build_absolute_uri(reverse(view_name))


class MainPageView(LoginRequiredMixin, TemplateView):
    template_name = "payments/main.html"


class SubscriptionPageView(LoginRequiredMixin, TemplateView):
    template_name = "payments/subscription/main.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        products = []
        for p in Product.objects.filter(active=True):
            prices = p.prices.filter(active=True)
            price = prices.first() if len(prices) else None

            # subscriptions = Subscription.objects.filter(active=True)

            product = {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "image": p.images[0] if p.images else None,
                "subscribed": False,
            }
            if price:
                product["price"] = {
                    "unit_amount": f"{price.unit_amount_decimal/100:.2f}",
                    "currency": price.currency,
                    "interval": price.recurring["interval"],
                }

            products.append(product)

        context["products"] = products
        return context


class SubscriptionSuccessPageView(SubscriptionPageView):
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        messages.success(request, "Profile details updated.")
        return render(request, self.template_name, context=context)


class SubscriptionCancelledPageView(SubscriptionPageView):
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        messages.warning(request, "Your payment was cancelled.")
        return render(request, self.template_name, context=context)


class CustomerPortalPageView(LoginRequiredMixin, TemplateView):
    template_name = "payments/customer-portal.html"


@login_required
@csrf_exempt
def stripe_config(request):
    """
    ref: https://stripe.com/docs/billing/subscriptions/integrating-customer-portal
    """
    if request.method == "GET":
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


# STRIPE


@login_required
@csrf_exempt
def stripe_subscription(request, product_id=1):
    if request.method == "GET":
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address
            #   details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see:
            #   https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect
            # will have the session ID set as a query param
            customer = Customer.objects.get(subscriber=request.user)
            product = Product.objects.get(id=product_id)
            checkout_session = stripe.checkout.Session.create(
                # new
                client_reference_id=customer.id,
                success_url=(
                    _get_payments_url(request, "payments:subscription-success")
                    + "?session_id={CHECKOUT_SESSION_ID}"
                ),
                cancel_url=(
                    _get_payments_url(
                        request, "payments:subscription-cancelled"
                    )
                ),
                payment_method_types=["card"],
                mode="subscription",
                line_items=[
                    {"price": product.prices.first().id, "quantity": 1}
                ],
            )
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})


""" @csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200) """


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def stripe_customer_portal(request):
    customer = Customer.objects.get(subscriber=request.user)

    PAYMENTS_URL = _get_payments_url(
        request, view_name="payments:customer-portal"
    )

    # Authenticate your user.
    session = stripe.billing_portal.Session.create(
        customer=customer.id,
        return_url=f"{PAYMENTS_URL}",
    )
    return HttpResponseRedirect(session.url)


# @login_required
# @require_http_methods(["POST"])
# @csrf_exempt
# def stripe_customer_portal(request):
#     stripe.Account.create(
#         country="US",
#         type="express",
#         capabilities={
#             "card_payments": {"requested": True},
#             "transfers": {"requested": True},
#         },
#         business_type="individual",
#         business_profile={"url": "https://example.com"},
#     )


# DJ Stripe


@webhooks.handler("customer.deleted")
def customer_deleted_event_listener(event, **kwargs):
    send_mail(
        "Subscription Deleted",
        "See ya! 👋",
        "from@example.com",
        ["to@example.com"],
        fail_silently=False,
    )
