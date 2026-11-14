class OrderBuilder:
    def add_items(self, cart):
        return self

    def set_address(self, address):
        return self

    def apply_coupon(self, code):
        return self

    def build(self):
        pass  # Karuna: return a finished Order


class OrderDirector:
    def __init__(self, builder):
        self.builder = builder

    def build_standard(self, cart, address):
        pass

    def build_gift(self, cart, address):
        pass