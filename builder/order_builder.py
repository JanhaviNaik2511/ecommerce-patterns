
from uuid import uuid4
from domain.order import Order, OrderItem


class OrderBuilder:
    def __init__(self):
        self.items = []
        self.total = 0
        self.address = None
        self.coupon_code = None
        self.is_gift = False

    def add_items(self, cart):
        self.items = [
            OrderItem(
                item.product.sku,
                item.quantity,
                item.product.price
            )
            for item in cart.items
        ]

        self.total = cart.get_total()
        return self

    def set_address(self, address):
        self.address = address
        return self

    def apply_coupon(self, code):
        self.coupon_code = code
        return self

    def build(self):
        order = Order(
            order_id=str(uuid4()),
            total=self.total,
            items=self.items
        )

        order.address = self.address
        order.coupon_code = self.coupon_code
        order.is_gift = self.is_gift

        return order


class OrderDirector:
    def __init__(self, builder):
        self.builder = builder

    def build_standard(self, cart, address):
        self.builder.is_gift = False

        return (
            self.builder
            .add_items(cart)
            .set_address(address)
            .build()
        )

    def build_gift(self, cart, address):
        self.builder.is_gift = True

        return (
            self.builder
            .add_items(cart)
            .set_address(address)
            .build()
        )
