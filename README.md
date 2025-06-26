# PrimeTrade AI Bot – Binance Futures Testnet

A simplified Python-based crypto trading bot that lets you place Binance Futures USDT-M orders via both command-line and a lightweight Streamlit UI.  Perfect for algorithmic trading experimentation with simulated funds.

---

## Features

- 🔐 Secure API credential handling (manual or .env)
- ✅ Supports Market, Limit, Stop, and Stop-Market order types
- 🔄 Buy/Sell support for USDT-M pairs (e.g., BTCUSDT)
- 📊 Real-time open order viewing in UI
- 📦 Command-line interface: main.py
- 🖥️ Streamlit-based frontend: app.py
- 📜 Logging of API responses & errors (bot.log)
- ⚙️ Built using official Binance API (python-binance)

---

## Project Structure
```
primetrade-ai-bot/
├── app.py             # Streamlit UI interface
├── main.py         # CLI interface to place orders
├── requirements.txt   # Python dependencies
├── trading.log            # Log of API interactions and errors
├── bot.py               # Core Bot logoc
└── .env               # Environment file for API credentials (not included in repo)

```


---

## Quick Start

1. 🔁 Clone the repo
```bash
git clone https://github.com/SS-Hossain/primetrade-ai-bot.git
cd primetrade-ai-bot
```

## Create & activate a virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
```
## Install dependencies
```bash
pip install -r requirements.txt
```

## Set your API key and secret (manually in the UI or via .env file):
# .env
```
API_KEY=your_api_key_here
API_SECRET=your_api_secret_here
```
## Run the App
🖥️ GUI (Streamlit):
```bash
streamlit run app.py
```

🖥️ CLI:
```bash
python run_bot.py
```

## Testnet Setup
- Uses Binance Futures Testnet (https://testnet.binancefuture.com)
- Generate API keys from your testnet account
- No real funds at risk — perfect for experimentation!


## Logs
Every action the bot takes — whether placing an order, receiving an API response, or encountering an error — is recorded in:

- Order requests
- Binance API responses
- Errors & exceptions

##  Bonus Features
-  Real-time display of active orders within the Streamlit dashboard
-  Robust error handling and input checks to minimize failures
