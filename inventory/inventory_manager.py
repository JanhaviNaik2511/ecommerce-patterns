class InventoryManager:
    @classmethod
    def get_instance(cls):
        pass  # Disha: return the single shared instance

    def add_stock(self, sku, qty):
        pass

    def reserve(self, sku, qty):
        return True

    def release(self, sku, qty):
        pass