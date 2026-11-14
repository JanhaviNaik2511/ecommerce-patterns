class CheckoutRequest:
    """Data object passed through the validation chain."""

    def __init__(self, cart, address, coupon_code=None, payment_method=None):
        self.cart = cart
        self.address = address
        self.coupon_code = coupon_code
        self.payment_method = payment_method