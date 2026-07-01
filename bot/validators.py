VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def validate_order_input(symbol, side, order_type, quantity, price=None):
    symbol = symbol.upper()
    side = side.upper()
    order_type = order_type.upper()

    if not symbol:
        raise ValueError("Symbol is required.")

    if side not in VALID_SIDES:
        raise ValueError("Side must be BUY or SELL.")

    if order_type not in VALID_ORDER_TYPES:
        raise ValueError("Order type must be MARKET or LIMIT.")

    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")

    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT order.")
        if price <= 0:
            raise ValueError("Price must be greater than 0 for LIMIT order.")
    elif order_type == "MARKET":
        price = None

    return {
        "symbol": symbol,
        "side": side,
        "order_type": order_type,
        "quantity": quantity,
        "price": price,
    }