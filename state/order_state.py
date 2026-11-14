from abc import ABC, abstractmethod


class OrderState(ABC):
    @abstractmethod
    def next(self, order):
        pass

    @abstractmethod
    def cancel(self, order):
        pass


class PlacedState(OrderState):
    def next(self, order):
        pass

    def cancel(self, order):
        pass


class PaidState(OrderState):
    def next(self, order):
        pass

    def cancel(self, order):
        pass


class ShippedState(OrderState):
    def next(self, order):
        pass

    def cancel(self, order):
        pass


class DeliveredState(OrderState):
    def next(self, order):
        pass

    def cancel(self, order):
        pass