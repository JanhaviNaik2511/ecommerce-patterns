# State and Observer Patterns

Part of the E-Commerce design patterns project.
Files: `state/order_state.py`, `observer/observers.py`, `tests/test_state_observer.py`

## State Pattern

An order behaves differently depending on its current state, so there are no big if/else chains. `Order` passes `next()` and `cancel()` to its current state object.

| State | next() | cancel() |
| --- | --- | --- |
| PlacedState | moves to Paid | moves to Cancelled |
| PaidState | moves to Shipped | moves to Cancelled |
| ShippedState | moves to Delivered | blocked |
| DeliveredState | no next state | blocked |
| CancelledState | no next state | already cancelled |

Every state change goes through `order.set_state()`.

## Observer Pattern

`order.set_state()` calls `notify_all()`, which calls `update(order)` on every attached observer.

| Observer | Output |
| --- | --- |
| EmailService | `[Email] Order <id> is now <state>` |
| SmsService | `[SMS] Order <id> is now <state>` |
| PushService | `[Push] Order <id> is now <state>` |

## Usage

```python
from domain.order import Order
from state.order_state import PlacedState
from observer.observers import EmailService, SmsService, PushService

order = Order("ORD1", 100, state=PlacedState())
order.attach(EmailService())
order.attach(SmsService())
order.attach(PushService())

order.next()    # Paid, all three observers print
order.next()    # Shipped
order.cancel()  # blocked: already shipped
```

Orders must start with `state=PlacedState()`. Without it, `Order` uses its temporary placeholder state.

## Tests

```
pytest tests/test_state_observer.py -q
```

6 tests cover the state flow, cancel rules, observer notifications and detaching an observer.