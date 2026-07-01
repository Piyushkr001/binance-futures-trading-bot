# Binance Futures Testnet Trading Bot

## Objective
This project is a simplified Python CLI trading bot for the Binance Futures Testnet. It provides an automated way to place MARKET and LIMIT orders, validate inputs, interact securely with the Binance API, and log all activities without exposing sensitive credentials. This project was built as part of a Python Developer Intern assignment.

## Features
- **Place MARKET orders:** Execute immediate orders at current market prices.
- **Place LIMIT orders:** Place orders at a specified price, using GTC (Good Till Canceled).
- **Supports BUY and SELL:** Both order sides are fully supported.
- **CLI Input Validation:** Ensures all parameters (symbol, side, type, quantity, price) are strictly validated before making API requests.
- **Secure API Integration:** Uses HMAC SHA256 signed requests as required by Binance. Does not leak secrets in logs.
- **Comprehensive Logging:** Logs API requests, responses, network errors, and validations clearly to `logs/trading_bot.log`.
- **Clean CLI Output:** Prints a readable summary of the order request and the subsequent response from Binance.

## Tech Stack
- **Python 3.x**
- **requests:** For making HTTP requests to the Binance Futures API.
- **python-dotenv:** For securely managing environment variables.

## Project Structure
```text
binance-futures-trading-bot/
├── bot/
│   ├── __init__.py
│   ├── client.py
│   ├── orders.py
│   ├── validators.py
│   └── logging_config.py
├── logs/
│   └── trading_bot.log
├── cli.py
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore
```

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd binance-futures-trading-bot
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy the `.env.example` file to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and fill in your Binance Futures Testnet API key and secret.

## Environment Variables
The bot requires the following environment variables (defined in `.env`):
- `BINANCE_API_KEY`: Your Binance Futures Testnet API Key.
- `BINANCE_API_SECRET`: Your Binance Futures Testnet API Secret.
- `BINANCE_BASE_URL`: The API base URL, typically `https://testnet.binancefuture.com`.

## How to run a MARKET order
To execute a MARKET order, run the following command (no price required):
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

## How to run a LIMIT order
To execute a LIMIT order, specify the `--price` argument:
```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 60000
```

## Sample Output
```text
Order Request Summary
---------------------
Symbol     : BTCUSDT
Side       : BUY
Order Type : LIMIT
Quantity   : 0.001
Price      : 60000.0

Sending order to Binance Futures Testnet...

Order Response
--------------
Order ID     : 1234567890
Status       : NEW
Executed Qty : 0.0000
Average Price: N/A

Order placed successfully.
```

## Logs
The bot automatically logs all significant events to `logs/trading_bot.log`. 
- **Request Summaries:** Logs parameters safely (excluding signature/secret).
- **Responses:** Logs response status code and body.
- **Errors:** Logs validation, API, and network errors.

## Assumptions
- The bot interacts strictly with the Binance Futures **Testnet**.
- It is assumed that the provided API credentials have proper permissions for trading on the testnet.
- LIMIT orders are hardcoded to `timeInForce=GTC` (Good Till Canceled).

## Security Notes
- The `.env` file containing API keys is excluded from version control via `.gitignore`.
- API signatures are generated locally via HMAC SHA256 and are intentionally stripped from log outputs to ensure credential safety.
- The `API_SECRET` is never transmitted directly in the request headers or body.

## Submission Notes
- To submit this project, ensure the `.env`, `venv/`, `__pycache__/`, and `.git/` directories are not included in your ZIP archive.
- Ensure `logs/trading_bot.log` contains a sample of your test runs as proof of execution.