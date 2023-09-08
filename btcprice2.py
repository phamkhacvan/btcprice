import requests
import json
import time
from telegram import Bot
from flask import Flask, render_template
import asyncio
import threading

app = Flask(__name__)

bot = Bot(token="6163331718:AAG7J467TQi53Xie1b9nAnnRP4sbJmlhiOY")
chat_id = "974909109"

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

async def send_price_message():
    while True:
        bitcoin_price = get_binance_price("BTCUSDT")
        # etherium_price = get_binance_price("ETHUSDT")
        message = f"Giá Bitcoin: {bitcoin_price}"
        # message = f"Giá Bitcoin: {bitcoin_price}  \nGiá Ethereum: {etherium_price}"
        await bot.send_message(chat_id=chat_id, text=message)
        await asyncio.sleep(60)  # Sử dụng asyncio.sleep để không chặn luồng

# Tạo một luồng riêng biệt để chạy coroutine send_price_message
def run_send_price_message():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_price_message())

# Khởi tạo luồng và chạy send_price_message trong nó
message_thread = threading.Thread(target=run_send_price_message)
message_thread.daemon = True  # Chạy dưới chế độ daemon để nó tự động kết thúc khi chương trình chính kết thúc
message_thread.start()

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
