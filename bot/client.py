import time
import hmac
import hashlib
from urllib.parse import urlencode

import requests

from bot.logging_config import setup_logger


class BinanceAPIError(Exception):
    pass


class BinanceFuturesClient:
    def __init__(self, api_key, api_secret, base_url):
        if not api_key or not api_secret:
            raise ValueError("API key and API secret are required.")

        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.logger = setup_logger()

    def _generate_signature(self, params):
        query_string = urlencode(params)
        return hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

    def _send_signed_request(self, method, endpoint, params):
        params["timestamp"] = int(time.time() * 1000)
        params["recvWindow"] = 5000
        params["signature"] = self._generate_signature(params)

        headers = {
            "X-MBX-APIKEY": self.api_key
        }

        url = f"{self.base_url}{endpoint}"

        safe_params = params.copy()
        safe_params.pop("signature", None)

        self.logger.info(f"API Request | {method} {endpoint} | params={safe_params}")

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                timeout=10
            )

            try:
                data = response.json()
            except ValueError:
                data = {"raw_response": response.text}

            self.logger.info(
                f"API Response | status_code={response.status_code} | response={data}"
            )

            if response.status_code >= 400:
                error_msg = data.get("msg", data.get("raw_response", "Unknown API error"))
                error_code = data.get("code", response.status_code)
                raise BinanceAPIError(f"[{error_code}] {error_msg}")

            return data

        except requests.exceptions.RequestException as error:
            self.logger.error(f"Network Error | {str(error)}")
            raise BinanceAPIError(f"Network error: {str(error)}")

    def create_order(self, symbol, side, order_type, quantity, price=None):
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT" and price is not None:
            params["price"] = price
            params["timeInForce"] = "GTC"

        return self._send_signed_request(
            method="POST",
            endpoint="/fapi/v1/order",
            params=params
        )