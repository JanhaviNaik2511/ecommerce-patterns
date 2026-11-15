# E-Commerce Design Patterns

A working in-memory E-Commerce backend in Python (FastAPI) where one checkout call passes through seven design patterns. A console demo (`main.py`) and a REST API (`app.py`) show the full flow.

## Checkout flow

Cart → (Strategy: discount) → total
`CheckoutFacade.place_order()`:
1. Validate: Stock → Address → Coupon → Fraud (Chain of Responsibility)
2. Reserve stock (Singleton)
3. Create the order (Builder)
4. Attach Email / SMS / Push observers (Observer)
5. Mock payment, order becomes Paid (State)

Order life cycle: Placed → Paid → Shipped → Delivered (cancel allowed only in Placed and Paid).

## Design patterns used

| Pattern | Type | Class(es) | File | Problem solved |
|---|---|---|---|---|
| Facade | Structural | CheckoutFacade | facade/checkout_facade.py | Hides the many checkout steps behind one `place_order()` call |
| Chain of Responsibility | Behavioural | ValidationHandler, StockCheck, AddressCheck, CouponCheck, FraudCheck | chain/handlers.py | Runs checks one by one, stops at the first failure, checks can be added or reordered |
| Singleton | Creational | InventoryManager | inventory/inventory_manager.py | One shared stock store for the whole app |
| Strategy | Behavioural | PricingStrategy, FlatDiscount, PercentageDiscount, BuyOneGetOne | pricing/strategies.py | Discount algorithms can be switched at runtime |
| Builder | Creational | OrderBuilder, OrderDirector | builder/order_builder.py | Builds an Order step by step; the Director holds ready-made recipes |
| State | Behavioural | OrderState, PlacedState, PaidState, ShippedState, DeliveredState | state/order_state.py | Order behaviour (next, cancel) depends on its current state |
| Observer | Behavioural | OrderObserver, EmailService, SmsService, PushService | observer/observers.py | Notifies services whenever the order state changes |

## Project structure

```
ecommerce-patterns/
├── app.py            FastAPI application
├── main.py           console demo
├── requirements.txt
├── domain/           User, Product, Cart, Order, CheckoutRequest
├── facade/           CheckoutFacade
├── chain/            validation handlers
├── inventory/        InventoryManager (Singleton)
├── pricing/          pricing strategies
├── builder/          OrderBuilder, OrderDirector
├── state/            order states
├── observer/         notification services
└── tests/            pytest tests
```

## How to run

```bash
pip install -r requirements.txt
python main.py            # console demo
pytest -q                 # all tests
uvicorn app:app --reload  # API, then open http://127.0.0.1:8000/docs
```

## API endpoints

| Endpoint | Purpose |
|---|---|
| GET /health | Check the service is running |
| POST /checkout | Place an order |
| GET /orders/{id} | View an order and its state |
| POST /orders/{id}/next | Move the order to the next state |
| POST /orders/{id}/cancel | Cancel (only in Placed or Paid) |
| GET /docs | Swagger page to test everything |

Live URL: _add the Render link here after deployment_

## Team

| Member | Module |
|---|---|
| Janhavi | Skeleton, domain, Facade, API, deployment |
| Disha | Chain of Responsibility, Singleton |
| Karuna | Strategy, Builder |
| Saini | State, Observer |