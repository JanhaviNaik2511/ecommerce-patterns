# E-Commerce Design Patterns
## Karuna Gauns – Strategy and Builder Patterns

### Files Implemented

**1. `pricing/strategies.py`**
- Implemented the PricingStrategy base class.
- Implemented FlatDiscount.
- Implemented PercentageDiscount.
- Implemented BuyOneGetOne.

**2. `builder/order_builder.py`**
- Implemented OrderBuilder.
- Implemented OrderDirector.
- Added standard order and gift order creation.

**3. `tests/test_strategy_builder.py`**
- Added tests for all three pricing strategies.
- Added tests for standard and gift order creation.
- All 5 tests passed successfully.

### Testing

Command used:

```bash
pytest -q
```

Result: 5 passed.
