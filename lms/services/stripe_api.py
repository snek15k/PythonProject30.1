import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def create_stripe_product(name: str):
    return stripe.Product.create(name=name)


def create_stripe_price(product_id: str, amount: int, currency='rub'):
    return stripe.Price.create(
        product=product_id,
        unit_amount=amount,
        currency=currency,
    )


def create_checkout_session(price_id: str, success_url: str, cancel_url: str):
    return stripe.checkout.Session.create(
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
