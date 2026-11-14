from abc import ABC, abstractmethod


class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, cart):
        pass


class FlatDiscount(PricingStrategy):
    def __init__(self, amount):
        self.amount = amount

    def calculate(self, cart):
        return cart.get_subtotal()


class PercentageDiscount(PricingStrategy):
    def __init__(self, percent):
        self.percent = percent

    def calculate(self, cart):
        return cart.get_subtotal()


class BuyOneGetOne(PricingStrategy):
    def calculate(self, cart):
        return cart.get_subtotal()