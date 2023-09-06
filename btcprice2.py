import requests
import json
import time
# from telegram import Bot
from flask import Flask, render_template

app = Flask(__name__)

# bot = Bot(token="YOUR_BOT_TOKEN")
# chat_id = "YOUR_CHAT_ID"

def get_binance_price(symbol="BTCUSDT"):
    base_url = "https://data.binance.com/api/v3/ticker/price"
    params = {"symbol": symbol}
    
    try:
        response = requests.get(base_url, params=params)
        data = json.loads(response.text)
        return float(data["price"])
    except Exception as e:
        print(f"Lỗi khi lấy giá: {e}")
        return None

@app.route('/')
def display_prices():
    bitcoin_price = get_binance_price("BTCUSDT")
    etherium_price = get_binance_price("ETHUSDT")
    return render_template('btcprice2.html', bitcoin_price=bitcoin_price, etherium_price=etherium_price)

@app.route('/get_bitcoin_price')
def get_bitcoin_price_json():
    bitcoin_price = get_binance_price("BTCUSDT")
    return {'bitcoin_price': bitcoin_price}

@app.route('/get_etherium_price')
def get_etherium_price_json():
    etherium_price = get_binance_price("ETHUSDT")
    return {'etherium_price': etherium_price}

if __name__ == "__main__":
    app.run(debug=True)
