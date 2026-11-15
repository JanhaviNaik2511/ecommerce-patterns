from inventory.inventory_manager import InventoryManager
import re
from abc import ABC, abstractmethod


class ValidationHandler(ABC):
    def set_next(self, handler):
        self.next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request):
        pass



class StockCheck(ValidationHandler):
    def handle(self, request):
        inventory = InventoryManager.get_instance()

        for item in request.cart.items:
            sku = item.product.sku
            quantity = item.quantity

            with inventory.stock_lock:
                available = inventory.stock.get(sku, 0)

            if available < quantity:
                return False

        if hasattr(self, "next_handler"):
            return self.next_handler.handle(request)

        return True




class AddressCheck(ValidationHandler):
    def handle(self, request):
        address = request.address

        if not address or not isinstance(address, str):
            return False

        if not re.search(r"\b\d{6}\b", address):
            return False

        if hasattr(self, "next_handler"):
            return self.next_handler.handle(request)

        return True




class CouponCheck(ValidationHandler):
    def handle(self, request):
        valid_coupons = ["SAVE10", "FLAT50"]

        coupon = request.coupon_code

        if coupon and coupon not in valid_coupons:
            return False

        if hasattr(self, "next_handler"):
            return self.next_handler.handle(request)

        return True




class FraudCheck(ValidationHandler):
    def handle(self, request):
        fraud_limit = 100000

        if request.cart.get_total() > fraud_limit:
            return False

        if hasattr(self, "next_handler"):
            return self.next_handler.handle(request)

        return True
