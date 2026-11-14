import pytest
from domain.product import Product
from domain.cart import Cart
from inventory.inventory_manager import InventoryManager
from facade.checkout_facade import CheckoutFacade

ADDRESS = "12 MG Road, Panaji, Goa 403001"


def make_cart(qty):
    cart = Cart()
    cart.add_item(Product("T1", "Test Pen", 50), qty)
    return cart


def test_place_order_success():
    InventoryManager.get_instance().add_stock("T1", 10)
    order = CheckoutFacade().place_order(make_cart(2), ADDRESS, "UPI")
    assert order is not None
    assert order.state.__class__.__name__ == "PaidState"


def test_place_order_rejected_when_out_of_stock():
    with pytest.raises(ValueError):
        CheckoutFacade().place_order(make_cart(9999), ADDRESS, "UPI")