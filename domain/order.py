class OrderItem:
    """One line in a placed order."""

    def __init__(self, sku, quantity, price):
        self.sku = sku
        self.quantity = quantity
        self.price = price

    def get_subtotal(self):
        return self.price * self.quantity


class _PlaceholderState:
    """Temporary state. Delete it once  real states (state/order_state.py) are merged."""

    def next(self, order):
        print("Placeholder state: next() not implemented yet")

    def cancel(self, order):
        print("Placeholder state: cancel() not implemented yet")


class Order:
    """Central object. Behaviour goes to its state; changes go to its observers."""

    def __init__(self, order_id, total, items=None, state=None):
        self.id = order_id
        self.total = total
        self.items = items if items is not None else []
        self.state = state if state is not None else _PlaceholderState()
        self.observers = []
        # Optional details the Builder can fill in
        self.address = None
        self.coupon_code = None
        self.is_gift = False

    # --- State pattern: just pass the call to the current state ---
    def next(self):
        self.state.next(self)

    def cancel(self):
        self.state.cancel(self)

    def set_state(self, new_state):
        self.state = new_state
        self.notify_all()  # tell every observer about the change

    # --- Observer pattern ---
    def attach(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def detach(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_all(self):
        for observer in self.observers:
            observer.update(self)