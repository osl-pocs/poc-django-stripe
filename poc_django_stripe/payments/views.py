from django.conf import settings
from django.http.response import (
    JsonResponse,
    HttpResponse,
    HttpResponseRedirect,
)
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView
from django.urls import reverse

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def _get_payments_url(request, view_name="payments:main"):
    return request.build_absolute_uri(reverse(view_name))


class CheckoutPageView(TemplateView):
    template_name = "checkout.html"


class CheckoutSuccessPageView(TemplateView):
    template_name = "checkout-success.html"


class CheckoutCancelledPageView(TemplateView):
    template_name = "checkout-cancelled.html"


class CustomerPortalPageView(TemplateView):
    template_name = "customer-portal.html"


@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


# STRIPE


@csrf_exempt
def stripe_checkout_session(request):
    PAYMENTS_URL = _get_payments_url(request)

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
            checkout_session = stripe.checkout.Session.create(
                # new
                client_reference_id=request.user.id
                if request.user.is_authenticated
                else None,
                success_url=PAYMENTS_URL
                + "checkout-success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=PAYMENTS_URL + "checkout-cancelled/",
                payment_method_types=["card"],
                mode="payment",
                line_items=[
                    {
                        "name": "T-shirt",
                        "quantity": 1,
                        "currency": "usd",
                        "amount": "2000",
                    }
                ],
            )
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})


@csrf_exempt
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

    return HttpResponse(status=200)


@require_http_methods(["POST"])
@csrf_exempt
def stripe_customer_portal(request):
    PAYMENTS_URL = _get_payments_url(
        request, view_name="payments:customer-portal"
    )

    # Authenticate your user.
    CUSTOMER_ID = "cus_L2PAyHZPQVWCKc"
    session = stripe.billing_portal.Session.create(
        customer=f"{CUSTOMER_ID}",
        return_url=f"{PAYMENTS_URL}",
    )
    return HttpResponseRedirect(session.url)
