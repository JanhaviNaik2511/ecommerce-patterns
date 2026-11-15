from domain.order import Order
from state.order_state import (
    PlacedState,
    PaidState,
    ShippedState,
    DeliveredState,
    CancelledState,
)
from observer.observers import EmailService, SmsService, PushService


def make_order():
    return Order("ORD1", 100, state=PlacedState())


# ---------- State pattern ----------

def test_next_moves_through_all_states():
    order = make_order()
    order.next()
    assert isinstance(order.state, PaidState)
    order.next()
    assert isinstance(order.state, ShippedState)
    order.next()
    assert isinstance(order.state, DeliveredState)


def test_cancel_allowed_when_placed():
    order = make_order()
    order.cancel()
    assert isinstance(order.state, CancelledState)


def test_cancel_allowed_when_paid():
    order = make_order()
    order.next()
    order.cancel()
    assert isinstance(order.state, CancelledState)


def test_cancel_blocked_after_shipped():
    order = make_order()
    order.next()
    order.next()
    order.cancel()
    assert isinstance(order.state, ShippedState)


# ---------- Observer pattern ----------

def test_observers_are_notified_on_state_change(capsys):
    order = make_order()
    order.attach(EmailService())
    order.attach(SmsService())
    order.attach(PushService())
    order.next()
    output = capsys.readouterr().out
    assert "[Email] Order ORD1 is now Paid" in output
    assert "[SMS] Order ORD1 is now Paid" in output
    assert "[Push] Order ORD1 is now Paid" in output


def test_detached_observer_is_not_notified(capsys):
    order = make_order()
    email = EmailService()
    order.attach(email)
    order.detach(email)
    order.next()
    assert capsys.readouterr().out == ""