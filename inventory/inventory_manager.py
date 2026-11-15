
import threading


class InventoryManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.stock = {}
                cls._instance.stock_lock = threading.Lock()

        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls()

    def add_stock(self, sku, qty):
        with self.stock_lock:
            self.stock[sku] = self.stock.get(sku, 0) + qty

    def reserve(self, sku, qty):
        with self.stock_lock:
            if self.stock.get(sku, 0) < qty:
                return False

            self.stock[sku] -= qty
            return True

    def release(self, sku, qty):
        with self.stock_lock:
            self.stock[sku] = self.stock.get(sku, 0) + qty
