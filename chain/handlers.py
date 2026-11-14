from abc import ABC, abstractmethod


class ValidationHandler(ABC):
    def set_next(self, handler):
        pass  # Disha: store the next handler and return it

    @abstractmethod
    def handle(self, request):
        pass


class StockCheck(ValidationHandler):
    def handle(self, request):
        return True


class AddressCheck(ValidationHandler):
    def handle(self, request):
        return True


class CouponCheck(ValidationHandler):
    def handle(self, request):
        return True


class FraudCheck(ValidationHandler):
    def handle(self, request):
        return True