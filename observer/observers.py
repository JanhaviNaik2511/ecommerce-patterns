from abc import ABC, abstractmethod


class OrderObserver(ABC):
    @abstractmethod
    def update(self, order):
        pass


class EmailService(OrderObserver):
    def update(self, order):
        pass


class SmsService(OrderObserver):
    def update(self, order):
        pass


class PushService(OrderObserver):
    def update(self, order):
        pass