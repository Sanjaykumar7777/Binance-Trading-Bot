import os
import logging
from binance import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from dotenv import load_dotenv

load_dotenv()

class TradingBot:
    def __init__(self, testnet=True):
        """Initialize the trading bot with API credentials from .env"""
        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_API_SECRET')
        
        if not api_key or not api_secret:
            raise ValueError("API key and secret must be set in .env file")
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('trading_bot.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        self.client = Client(api_key, api_secret, testnet=testnet)
        self.logger.info("Trading bot initialized successfully")

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        """Place an order on Binance Futures"""
        try:
            self.logger.info(f"Placing order: {symbol} {side} {order_type} {quantity}")
            
            params = {
                'symbol': symbol,
                'side': side,
                'type': order_type,
                'quantity': quantity,
            }
            
            if order_type == 'LIMIT':
                params['price'] = price
                params['timeInForce'] = 'GTC'
            elif order_type == 'STOP':
                params['price'] = price
                params['stopPrice'] = stop_price
                params['timeInForce'] = 'GTC'
            
            response = self.client.futures_create_order(**params)
            self.logger.info(f"Order placed successfully: {response}")
            return response
            
        except BinanceAPIException as e:
            self.logger.error(f"Binance API Exception: {e.status_code} - {e.message}")
            raise
        except BinanceOrderException as e:
            self.logger.error(f"Binance Order Exception: {e.status_code} - {e.message}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            raise

    def get_account_balance(self):
        """Get futures account balance"""
        try:
            balance = self.client.futures_account_balance()
            usdt_balance = next((item for item in balance if item['asset'] == 'USDT'), None)
            return float(usdt_balance['balance']) if usdt_balance else 0.0
        except Exception as e:
            self.logger.error(f"Error getting balance: {str(e)}")
            return 0.0

    def get_open_orders(self, symbol=None):
        """Get current open orders"""
        try:
            if symbol:
                return self.client.futures_get_open_orders(symbol=symbol)
            return self.client.futures_get_open_orders()
        except Exception as e:
            self.logger.error(f"Error getting open orders: {str(e)}")
            return []

    def cancel_order(self, symbol, order_id):
        """Cancel an existing order"""
        try:
            return self.client.futures_cancel_order(symbol=symbol, orderId=order_id)
        except Exception as e:
            self.logger.error(f"Error canceling order: {str(e)}")
            raise