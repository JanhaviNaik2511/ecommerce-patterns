from chain.handlers import StockCheck, AddressCheck, CouponCheck, FraudCheck
from inventory.inventory_manager import InventoryManager
from builder.order_builder import OrderBuilder, OrderDirector
from state.order_state import PlacedState, PaidState
from observer.observers import EmailService, SmsService, PushService
from domain.checkout_request import CheckoutRequest


class CheckoutFacade:
    """One simple place_order() call that hides the whole checkout sequence."""

    def __init__(self):
        self.log = []  # shows each step (useful for the demo and API)

    def _build_chain(self):
        stock = StockCheck()
        stock.set_next(AddressCheck()).set_next(CouponCheck()).set_next(FraudCheck())
        return stock  # first handler of the chain

    def _mock_payment(self, order, method):
        self.log.append(f"Payment of {order.total} received via {method}")
        return True

    def place_order(self, cart, address, method, coupon_code=None):
        # 1. Validate (Chain of Responsibility)
        request = CheckoutRequest(cart, address, coupon_code, method)
        if not self._build_chain().handle(request):
            raise ValueError("Validation failed: order rejected")
        self.log.append("Validation passed")

        # 2. Reserve stock (Singleton)
        inventory = InventoryManager.get_instance()
        reserved = []
        for item in cart.items:
            if inventory.reserve(item.product.sku, item.quantity):
                reserved.append(item)
            else:
                for r in reserved:  # undo what was already reserved
                    inventory.release(r.product.sku, r.quantity)
                raise ValueError(f"Not enough stock for {item.product.sku}")
        self.log.append("Stock reserved")

        # 3. Build the order (Builder)
        if coupon_code:
            order = (OrderBuilder().add_items(cart).set_address(address)
                     .apply_coupon(coupon_code).build())
        else:
            order = OrderDirector(OrderBuilder()).build_standard(cart, address)
        self.log.append(f"Order {order.id} built")

        # 4. Attach observers (Observer)
        order.attach(EmailService())
        order.attach(SmsService())
        order.attach(PushService())

        # 5. Placed, then mock payment, then Paid (State)
        order.set_state(PlacedState())
        if self._mock_payment(order, method):
            order.set_state(PaidState())

        return order