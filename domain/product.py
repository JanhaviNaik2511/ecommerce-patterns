class Product:
    """An item that can be sold."""

    def __init__(self, sku, name, price):
        self.sku = sku
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product({self.sku}, {self.name}, {self.price})"


class Category:
    """Groups products (kept because it is in the class diagram)."""

    def __init__(self, name):
        self.name = name
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def get_products(self):
        return self.products