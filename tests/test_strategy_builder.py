
from builder.order_builder import OrderBuilder, OrderDirector
from domain.product import Product
from domain.cart import Cart
from pricing.strategies import (
    FlatDiscount,
    PercentageDiscount,
    BuyOneGetOne
)


def create_cart():
    product = Product("P101", "Laptop", 500)
    cart = Cart()
    cart.add_item(product, 2)
    return cart


def test_flat_discount():
    cart = create_cart()
    cart.set_strategy(FlatDiscount(100))

    assert cart.get_total() == 900


def test_percentage_discount():
    cart = create_cart()
    cart.set_strategy(PercentageDiscount(20))

    assert cart.get_total() == 800


def test_buy_one_get_one():
    cart = create_cart()
    cart.set_strategy(BuyOneGetOne())

    assert cart.get_total() == 500


def test_standard_order():
    cart = create_cart()
    builder = OrderBuilder()
    director = OrderDirector(builder)

    order = director.build_standard(cart, "Goa")

    assert order.total == 1000
    assert order.address == "Goa"
    assert len(order.items) == 1
    assert order.items[0].sku == "P101"
    assert order.is_gift is False


def test_gift_order():
    cart = create_cart()
    builder = OrderBuilder()
    director = OrderDirector(builder)

    order = director.build_gift(cart, "Goa")

    assert order.total == 1000
    assert order.address == "Goa"
    assert order.is_gift is True
