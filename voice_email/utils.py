import stripe


STRIPE_PUBLIC_KEY = 'pk_test_51OyRANSE615NBgftHqTOK0erhWj7ff4IXrXPkyPjjrw02CXcAeZs6abbkOfuUAcottmNSES83mTTPXKQ5CFVSWJC00uDNnnnfw' # change this
STRIPE_SECRET_KEY = 'sk_test_51OyRANSE615NBgftGE7BbVa53hyvZ9sVsusIS31tKBnnUmx3Sn7LgJnMxQ4b1t1XyUBN9V3auy7ggK8DYQvSBTzo00eeFz9vFB' # change this


def create_stripe_payment_link(amount):
    amount = int(amount)
    stripe.api_key = STRIPE_SECRET_KEY
    try:
        payment_link = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': 'RECHARGE WALLET',
                        },
                        'unit_amount': int(amount*100),  # Amount in cents
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url= "http://127.0.0.1:8000/accounts/success?amt="+str(amount)
            
        )
        return payment_link.url
    except stripe.error.StripeError as e:
        msg = f"🚫 PAYMENT LINK GENERATION FAILED -> {e}"
        print("MSG : ",msg)
        return None