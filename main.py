import argparse
import getpass
from bot import TradingBot
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    # Initialize bot
    try:
        bot = TradingBot()
        print("✅ Successfully connected to Binance Testnet")
    except Exception as e:
        print(f"❌ Failed to initialize bot: {str(e)}")
        return

    # Main menu
    while True:
        print("\n=== Binance Futures Trading Bot ===")
        print("1. Place New Order")
        print("2. View Open Orders")
        print("3. Check Account Balance")
        print("4. Cancel Order")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ")
        
        if choice == '1':
            place_order_menu(bot)
        elif choice == '2':
            view_orders_menu(bot)
        elif choice == '3':
            check_balance_menu(bot)
        elif choice == '4':
            cancel_order_menu(bot)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

def place_order_menu(bot):
    print("\n--- Place New Order ---")
    symbol = input("Trading pair (e.g. BTCUSDT): ").upper()
    side = input("Side (BUY/SELL): ").upper()
    order_type = input("Order type (MARKET/LIMIT/STOP): ").upper()
    quantity = float(input("Quantity: "))
    
    price = None
    stop_price = None
    
    if order_type in ['LIMIT', 'STOP']:
        price = float(input("Price: "))
    
    if order_type == 'STOP':
        stop_price = float(input("Stop Price: "))
    
    try:
        order = bot.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price
        )
        print("\n✅ Order placed successfully!")
        print(f"Order ID: {order['orderId']}")
        print(f"Status: {order['status']}")
    except Exception as e:
        print(f"\n❌ Failed to place order: {str(e)}")

def view_orders_menu(bot):
    print("\n--- Open Orders ---")
    symbol = input("Enter trading pair (leave empty for all): ").upper() or None
    try:
        orders = bot.get_open_orders(symbol)
        if not orders:
            print("No open orders found")
            return
            
        for order in orders:
            print(f"\n{symbol} {order['side']} {order['type']}")
            print(f"Order ID: {order['orderId']}")
            print(f"Quantity: {order['origQty']}")
            if 'price' in order:
                print(f"Price: {order['price']}")
            if 'stopPrice' in order:
                print(f"Stop Price: {order['stopPrice']}")
    except Exception as e:
        print(f"Error fetching orders: {str(e)}")

def check_balance_menu(bot):
    print("\n--- Account Balance ---")
    try:
        balance = bot.get_account_balance()
        print(f"USDT Balance: {balance:,.2f}")
    except Exception as e:
        print(f"Error fetching balance: {str(e)}")

def cancel_order_menu(bot):
    print("\n--- Cancel Order ---")
    symbol = input("Trading pair (e.g. BTCUSDT): ").upper()
    order_id = input("Order ID to cancel: ")
    try:
        result = bot.cancel_order(symbol, order_id)
        print(f"✅ Order {order_id} cancelled successfully!")
    except Exception as e:
        print(f"❌ Failed to cancel order: {str(e)}")

if __name__ == '__main__':
    main()