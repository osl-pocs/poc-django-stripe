import stripe


def test_stripe_api_base():
    stripe.api_base == "http://localhost:12111"
