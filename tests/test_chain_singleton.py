
from inventory.inventory_manager import InventoryManager
from chain.handlers import StockCheck, AddressCheck, CouponCheck, FraudCheck
from domain.cart import Cart
from domain.product import Product
from domain.checkout_request import CheckoutRequest


# Test 1: Check Singleton
def test_singleton_returns_same_instance():
    inventory1 = InventoryManager.get_instance()
    inventory2 = InventoryManager.get_instance()

    assert inventory1 is inventory2


# Test 2: Check stock reservation
def test_reserve_stock():
    inventory = InventoryManager.get_instance()

    inventory.add_stock("LAPTOP_TEST", 10)

    assert inventory.reserve("LAPTOP_TEST", 3) is True
    assert inventory.reserve("LAPTOP_TEST", 8) is False


# Test 3: Valid checkout passes through all handlers
def test_valid_checkout_passes_chain():
    inventory = InventoryManager.get_instance()

    product = Product("CHAIN_TEST_01", "Laptop", 50000)
    inventory.add_stock("CHAIN_TEST_01", 10)

    cart = Cart()
    cart.add_item(product, 2)

    request = CheckoutRequest(
        cart,
        "House 10, Canacona, Goa 403702",
        "SAVE10",
        "UPI"
    )

    stock = StockCheck()
    address = AddressCheck()
    coupon = CouponCheck()
    fraud = FraudCheck()

    stock.set_next(address).set_next(coupon).set_next(fraud)

    assert stock.handle(request) is True


# Test 4: Invalid coupon stops the chain
def test_invalid_coupon_stops_chain():
    inventory = InventoryManager.get_instance()

    product = Product("CHAIN_TEST_02", "Mouse", 500)
    inventory.add_stock("CHAIN_TEST_02", 10)

    cart = Cart()
    cart.add_item(product, 1)

    request = CheckoutRequest(
        cart,
        "House 10, Canacona, Goa 403702",
        "WRONG123",
        "UPI"
    )

    stock = StockCheck()
    address = AddressCheck()
    coupon = CouponCheck()
    fraud = FraudCheck()

    stock.set_next(address).set_next(coupon).set_next(fraud)

    assert stock.handle(request) is False
