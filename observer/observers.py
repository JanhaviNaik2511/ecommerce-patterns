from abc import ABC, abstractmethod


class OrderObserver(ABC):
    @abstractmethod
    def update(self, order):
        pass


class EmailService(OrderObserver):
    def update(self, order):
        print(f"[Email] Order {order.id} is now {order.state.name}")


class SmsService(OrderObserver):
    def update(self, order):
        print(f"[SMS] Order {order.id} is now {order.state.name}")


class PushService(OrderObserver):
    def update(self, order):
        print(f"[Push] Order {order.id} is now {order.state.name}")