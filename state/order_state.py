from abc import ABC, abstractmethod


class OrderState(ABC):
    name = "Unknown"

    @abstractmethod
    def next(self, order):
        pass

    @abstractmethod
    def cancel(self, order):
        pass


class PlacedState(OrderState):
    name = "Placed"

    def next(self, order):
        order.set_state(PaidState())

    def cancel(self, order):
        order.set_state(CancelledState())


class PaidState(OrderState):
    name = "Paid"

    def next(self, order):
        order.set_state(ShippedState())

    def cancel(self, order):
        order.set_state(CancelledState())


class ShippedState(OrderState):
    name = "Shipped"

    def next(self, order):
        order.set_state(DeliveredState())

    def cancel(self, order):
        print("Cannot cancel: order already shipped.")


class DeliveredState(OrderState):
    name = "Delivered"

    def next(self, order):
        print("Order is already delivered. No next state.")

    def cancel(self, order):
        print("Cannot cancel: order already delivered.")


class CancelledState(OrderState):
    name = "Cancelled"

    def next(self, order):
        print("Order is cancelled. No next state.")

    def cancel(self, order):
        print("Order is already cancelled.")