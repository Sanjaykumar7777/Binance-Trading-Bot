import streamlit as st
from bot import TradingBot
from dotenv import load_dotenv
import time

load_dotenv()

def main():
    st.set_page_config(page_title="Binance Trading Bot", layout="wide")
    
    st.title("📈 Binance Futures Trading Bot")
    st.markdown("""
    This app connects to the Binance Futures **Testnet** to place trades using API keys from .env file.
    All trades are executed with simulated funds.
    """)
    
    # Initialize session state
    if 'bot' not in st.session_state:
        try:
            st.session_state.bot = TradingBot()
            st.session_state.logged_in = True
        except Exception as e:
            st.error(f"Failed to initialize bot: {str(e)}")
            st.session_state.logged_in = False
    
    if st.session_state.logged_in:
        tab1, tab2, tab3 = st.tabs(["📊 Trade", "📋 Open Orders", "ℹ️ Account Info"])
        
        with tab1:
            trade_interface()
        
        with tab2:
            orders_interface()
        
        with tab3:
            account_interface()
    else:
        st.error("Please check your .env file configuration and restart the app")

def trade_interface():
    st.subheader("Place New Order")
    
    col1, col2 = st.columns(2)
    with col1:
        symbol = st.selectbox(
            "Trading Pair",
            ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"],
            index=0
        )
        order_type = st.selectbox(
            "Order Type",
            ["MARKET", "LIMIT", "STOP"],
            index=0
        )
    
    with col2:
        side = st.radio("Side", ["BUY", "SELL"], horizontal=True)
        quantity = st.number_input("Quantity", min_value=0.001, value=0.01, step=0.001)
    
    if order_type in ["LIMIT", "STOP"]:
        price = st.number_input("Price", min_value=0.01, value=1000.0 if "BTC" in symbol else 100.0, step=0.01)
    else:
        price = None
        
    if order_type == "STOP":
        stop_price = st.number_input("Stop Price", min_value=0.01, value=900.0 if "BTC" in symbol else 90.0, step=0.01)
    else:
        stop_price = None
    
    if st.button("Place Order"):
        with st.spinner("Placing order..."):
            try:
                order = st.session_state.bot.place_order(
                    symbol=symbol,
                    side=side,
                    order_type=order_type,
                    quantity=quantity,
                    price=price,
                    stop_price=stop_price
                )
                
                st.success("Order placed successfully!")
                st.json(order)
                
                cols = st.columns(2)
                cols[0].metric("Order ID", order['orderId'])
                cols[1].metric("Status", order['status'])
                st.metric("Quantity", f"{float(order['origQty']):,.3f} {symbol.replace('USDT', '')}")
                
                if 'price' in order:
                    st.metric("Price", f"{float(order['price']):,.2f}")
                if 'stopPrice' in order:
                    st.metric("Stop Price", f"{float(order['stopPrice']):,.2f}")
                
            except Exception as e:
                st.error(f"Failed to place order: {str(e)}")

def orders_interface():
    st.subheader("Current Open Orders")
    try:
        orders = st.session_state.bot.get_open_orders()
        
        if not orders:
            st.info("No open orders found")
        else:
            for order in orders:
                with st.expander(f"{order['symbol']} {order['side']} {order['type']}"):
                    cols = st.columns(3)
                    cols[0].metric("Order ID", order['orderId'])
                    cols[1].metric("Quantity", f"{float(order['origQty']):,.3f}")
                    cols[2].metric("Price", f"{float(order['price']):,.2f}" if 'price' in order else "Market")
                    
                    if order['type'] == 'STOP':
                        st.metric("Stop Price", f"{float(order['stopPrice']):,.2f}")
                    
                    if st.button(f"Cancel Order {order['orderId']}", key=f"cancel_{order['orderId']}"):
                        try:
                            result = st.session_state.bot.cancel_order(
                                symbol=order['symbol'],
                                orderId=order['orderId']
                            )
                            st.success(f"Order {order['orderId']} cancelled!")
                            time.sleep(1)
                            st.experimental_rerun()
                        except Exception as e:
                            st.error(f"Failed to cancel order: {str(e)}")
    except Exception as e:
        st.error(f"Error fetching orders: {str(e)}")

def account_interface():
    st.subheader("Account Information")
    try:
        balance = st.session_state.bot.get_account_balance()
        st.metric("USDT Balance", f"{balance:,.2f}")
        
        positions = st.session_state.bot.client.futures_position_information()
        if positions:
            st.subheader("Current Positions")
            for position in positions:
                if float(position['positionAmt']) != 0:
                    with st.expander(f"{position['symbol']} Position"):
                        cols = st.columns(3)
                        cols[0].metric("Size", f"{float(position['positionAmt']):,.3f}")
                        cols[1].metric("Entry Price", f"{float(position['entryPrice']):,.2f}")
                        cols[2].metric("Unrealized PnL", f"{float(position['unRealizedProfit']):,.2f}")
    except Exception as e:
        st.error(f"Error fetching account info: {str(e)}")

if __name__ == '__main__':
    main()