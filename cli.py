import argparse
import os

# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

from bot.client import BinanceFuturesClient, BinanceAPIError
from bot.orders import OrderService
from bot.logging_config import setup_logger


def print_order_summary(symbol, side, order_type, quantity, price):
    print("\nOrder Request Summary")
    print("---------------------")
    print(f"Symbol     : {symbol}")
    print(f"Side       : {side}")
    print(f"Order Type : {order_type}")
    print(f"Quantity   : {quantity}")

    if order_type == "LIMIT":
        print(f"Price      : {price}")


def print_order_response(response):
    print("\nOrder Response")
    print("--------------")
    print(f"Order ID     : {response.get('orderId', 'N/A')}")
    print(f"Status       : {response.get('status', 'N/A')}")
    print(f"Executed Qty : {response.get('executedQty', 'N/A')}")
    print(f"Average Price: {response.get('avgPrice', 'N/A')}")
    print("\nOrder placed successfully.")


def main():
    load_dotenv()
    logger = setup_logger()

    parser = argparse.ArgumentParser(
        description="Simplified Binance Futures Testnet Trading Bot"
    )

    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT"], help="Order type")
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument("--price", type=float, help="Price for LIMIT order")

    args = parser.parse_args()

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    base_url = os.getenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com")

    if not api_key or not api_secret:
        print("\nError: API credentials are missing.")
        print("Please ensure BINANCE_API_KEY and BINANCE_API_SECRET are set in your .env file.")
        logger.error("Missing API credentials.")
        return

    try:
        print_order_summary(
            symbol=args.symbol.upper(),
            side=args.side.upper(),
            order_type=args.type.upper(),
            quantity=args.quantity,
            price=args.price
        )

        print("\nSending order to Binance Futures Testnet...")

        client = BinanceFuturesClient(
            api_key=api_key,
            api_secret=api_secret,
            base_url=base_url
        )

        order_service = OrderService(client)

        response = order_service.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price
        )

        print_order_response(response)

    except ValueError as error:
        logger.error(f"Validation Error | {str(error)}")
        print(f"\nOrder failed: {str(error)}")

    except BinanceAPIError as error:
        logger.error(f"Binance API Error | {str(error)}")
        print("\nOrder failed due to Binance API error.")
        print(f"Reason: {error}")

    except Exception as error:
        logger.exception("Unexpected Error")
        print("\nOrder failed due to unexpected error.")
        print(f"Reason: {error}")


if __name__ == "__main__":
    main()