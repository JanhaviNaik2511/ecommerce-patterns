from domain.product import Product
from domain.cart import Cart
from inventory.inventory_manager import InventoryManager
from pricing.strategies import FlatDiscount, PercentageDiscount, BuyOneGetOne
from facade.checkout_facade import CheckoutFacade


def main():
    # --- Setup: products and stock (Singleton) ---
    pen = Product("P1", "Pen", 50)
    book = Product("B1", "Notebook", 120)

    inventory = InventoryManager.get_instance()
    inventory.add_stock("P1", 20)
    inventory.add_stock("B1", 10)

    # --- Cart and pricing (Strategy) ---
    cart = Cart()
    cart.add_item(pen, 4)
    cart.add_item(book, 2)

    print("=== PRICING (Strategy) ===")
    print("Total without discount:", cart.get_total())
    for name, strategy in [("Flat 50", FlatDiscount(50)),
                           ("10 percent", PercentageDiscount(10)),
                           ("Buy one get one", BuyOneGetOne())]:
        cart.set_strategy(strategy)
        print(f"Total with {name}:", cart.get_total())

    cart.set_strategy(PercentageDiscount(10))  # use this one for checkout
    print("\nChosen strategy: 10 percent ->", cart.get_total())

    # --- Checkout (Facade: Chain, Singleton, Builder, State, Observer) ---
    print("\n=== CHECKOUT (Facade) ===")
    facade = CheckoutFacade()
    address = "12 MG Road, Panaji, Goa 403001"
    order = facade.place_order(cart, address, "UPI", "SAVE10")

    for line in facade.log:
        print(" -", line)

    # --- Order life cycle (State + Observer) ---
    print("\n=== ORDER STATES ===")
    print("Next ->"); order.next()   # Paid -> Shipped
    print("Cancel attempt:"); order.cancel()   # should be blocked after Shipped
    print("Next ->"); order.next()   # Shipped -> Delivered
    print("Next ->"); order.next()   # already delivered message


if __name__ == "__main__":
    main()