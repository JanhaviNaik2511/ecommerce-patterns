class CartItem:
    """One line in a cart."""

    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def get_subtotal(self):
        return self.product.price * self.quantity


class Cart:
    """Holds items and lets the pricing strategy calculate the total."""

    def __init__(self):
        self.items = []
        self.strategy = None  # set later with set_strategy()

    def add_item(self, product, qty=1):
        # If the product is already in the cart, just increase the quantity
        for item in self.items:
            if item.product.sku == product.sku:
                item.quantity += qty
                return
        self.items.append(CartItem(product, qty))

    def remove_item(self, sku):
        self.items = [i for i in self.items if i.product.sku != sku]

    def set_strategy(self, strategy):
        self.strategy = strategy

    def get_subtotal(self):
        """Total BEFORE any discount (strategies can use this)."""
        return sum(item.get_subtotal() for item in self.items)

    def get_total(self):
        """Total AFTER discount. The strategy does the calculation."""
        if self.strategy is None:
            return self.get_subtotal()
        return self.strategy.calculate(self)