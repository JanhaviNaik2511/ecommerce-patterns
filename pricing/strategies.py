
from abc import ABC, abstractmethod


class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, cart):
        pass


class FlatDiscount(PricingStrategy):
    def __init__(self, amount):
        self.amount = amount

    def calculate(self, cart):
        total = cart.get_subtotal()
        return max(0, total - self.amount)


class PercentageDiscount(PricingStrategy):
    def __init__(self, percent):
        self.percent = percent

    def calculate(self, cart):
        total = cart.get_subtotal()
        discount = total * (self.percent / 100)
        return total - discount


class BuyOneGetOne(PricingStrategy):
    def calculate(self, cart):
        total = 0

        # One free item for every two units of the same product.
        for item in cart.items:
            paid_quantity = item.quantity - (item.quantity // 2)
            total += item.product.price * paid_quantity

        return total
