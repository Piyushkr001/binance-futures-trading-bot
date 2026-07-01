from bot.validators import validate_order_input


class OrderService:
    def __init__(self, client):
        self.client = client

    def place_order(self, symbol, side, order_type, quantity, price=None):
        validated_data = validate_order_input(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )

        return self.client.create_order(
            symbol=validated_data["symbol"],
            side=validated_data["side"],
            order_type=validated_data["order_type"],
            quantity=validated_data["quantity"],
            price=validated_data["price"]
        )