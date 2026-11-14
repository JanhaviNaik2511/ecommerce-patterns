from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from domain.product import Product
from domain.cart import Cart
from inventory.inventory_manager import InventoryManager
from pricing.strategies import FlatDiscount, PercentageDiscount, BuyOneGetOne
from facade.checkout_facade import CheckoutFacade

app = FastAPI(title="E-Commerce Design Patterns")

# --- In-memory data (no database) ---
CATALOGUE = {
    "P1": Product("P1", "Pen", 50),
    "B1": Product("B1", "Notebook", 120),
    "M1": Product("M1", "Mouse", 600),
}

STRATEGIES = {
    "flat": lambda: FlatDiscount(50),
    "percentage": lambda: PercentageDiscount(10),
    "bogo": lambda: BuyOneGetOne(),
}

orders = {}  # order id -> Order

inventory = InventoryManager.get_instance()
for sku in CATALOGUE:
    inventory.add_stock(sku, 100)


# --- Request format ---
class ItemIn(BaseModel):
    sku: str
    quantity: int


class CheckoutIn(BaseModel):
    items: List[ItemIn]
    address: str
    payment_method: str = "UPI"
    strategy: Optional[str] = None      # flat / percentage / bogo
    coupon_code: Optional[str] = None


def order_to_dict(order, log=None):
    data = {
        "order_id": order.id,
        "total": order.total,
        "state": type(order.state).__name__,
    }
    if log is not None:
        data["log"] = log
    return data


def get_order(order_id):
    order = orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# --- Endpoints ---
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/checkout")
def checkout(body: CheckoutIn):
    cart = Cart()
    for item in body.items:
        product = CATALOGUE.get(item.sku)
        if product is None:
            raise HTTPException(status_code=400, detail=f"Unknown product {item.sku}")
        cart.add_item(product, item.quantity)

    if body.strategy:
        if body.strategy not in STRATEGIES:
            raise HTTPException(status_code=400, detail="Strategy must be flat, percentage or bogo")
        cart.set_strategy(STRATEGIES[body.strategy]())

    facade = CheckoutFacade()
    try:
        order = facade.place_order(cart, body.address, body.payment_method, body.coupon_code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    orders[order.id] = order
    return order_to_dict(order, facade.log)


@app.get("/orders/{order_id}")
def read_order(order_id: str):
    return order_to_dict(get_order(order_id))


@app.post("/orders/{order_id}/next")
def next_state(order_id: str):
    order = get_order(order_id)
    order.next()
    return order_to_dict(order)


@app.post("/orders/{order_id}/cancel")
def cancel_order(order_id: str):
    order = get_order(order_id)
    try:
        order.cancel()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return order_to_dict(order)