
import requests
import json
import time
from telegram import Bot
from flask import Flask, render_template
import asyncio
import threading
from datetime import datetime


app = Flask(__name__)

bot = Bot(token="6163331718:AAG7J467TQi53Xie1b9nAnnRP4sbJmlhiOY")
chat_id = "974909109"


# Biến global để lưu giá Bitcoin từ mốc 0:00
bitcoin_price_0_am = None
previous_bitcoin_price = None

is_sending = False


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
    global bitcoin_price_0_am
    global previous_bitcoin_price
    
    while True:
        bitcoin_price = get_binance_price("BTCUSDT")

        current_time = datetime.now()
        zero_am = current_time.replace(hour=0, minute=0, second=0, microsecond=0)

        if bitcoin_price_0_am is None:
            bitcoin_price_0_am = bitcoin_price

        if previous_bitcoin_price is not None:
            price_change = bitcoin_price - previous_bitcoin_price
            if abs(price_change) >= 1:
                percent_change = (price_change / previous_bitcoin_price) * 100
                message = f"Giá Bitcoin: {bitcoin_price} USDT\nThay đổi: {percent_change:.2f}%"
                await bot.send_message(chat_id=chat_id, text=message)

        previous_bitcoin_price = bitcoin_price
        await asyncio.sleep(1)  # Thay đổi thời gian cần đợi ở đây nếu cần



    global is_sending  # Sử dụng biến cờ toàn cục
    while True:
        if not is_sending:
            is_sending = True  # Đánh dấu luồng đang gửi thông báo
            bitcoin_price = get_binance_price("BTCUSDT")
            message = f"Giá Bitcoin: {bitcoin_price}"
            await bot.send_message(chat_id=chat_id, text=message)
            is_sending = False  # Đánh dấu luồng đã hoàn thành
        await asyncio.sleep(60)

# Tạo một luồng riêng biệt để chạy coroutine send_price_message
def run_send_price_message():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_price_message())

# Khởi tạo luồng và chạy send_price_message trong nó
message_thread = threading.Thread(target=run_send_price_message)
message_thread.daemon = True  # Chạy dưới chế độ daemon để nó tự động kết thúc khi chương trình chính kết thúc
message_thread.start()

current_btc_price = get_binance_price("BTCUSDT")

# Giá BTC vào thời điểm cụ thể (0:00 ngày 11 tháng 9 năm 2023)
specific_datetime = datetime(2023, 9, 11, 0, 0)
specific_btc_price = get_binance_price("BTCUSDT")

if specific_btc_price is not None:
    # Tính phần trăm thay đổi
    price_change_percentage = ((current_btc_price - specific_btc_price) / specific_btc_price) * 100
    print(f"Phần trăm thay đổi giá BTC từ {specific_datetime} đến hiện tại là: {price_change_percentage:.2f}%")
else:
    print("Không thể lấy được giá BTC tại thời điểm cụ thể.")

@app.route('/')
def display_prices():
    bitcoin_price = get_binance_price("BTCUSDT")
    etherium_price = get_binance_price("ETHUSDT")
    return render_template('btcprice2.html', bitcoin_price=bitcoin_price, etherium_price=etherium_price)

@app.route('/get_bitcoin_price')
def get_bitcoin_price_json():
    bitcoin_price = get_binance_price("BTCUSDT")
    # Tính phần trăm thay đổi Bitcoin (BTC)
    percent_change_btc = ((bitcoin_price - bitcoin_price_0_am) / bitcoin_price_0_am) * 100
    return {'bitcoin_price': bitcoin_price, 'percent_change_btc': percent_change_btc}

@app.route('/get_etherium_price')
def get_etherium_price_json():
    etherium_price = get_binance_price("ETHUSDT")
    return {'etherium_price': etherium_price}

if __name__ == "__main__":
    app.run(debug=True)
    #jjjj
    
@app.route('/')
def display_prices():
    current_btc_price = get_binance_price("BTCUSDT")
    specific_datetime = datetime(2023, 9, 11, 0, 0)
    specific_btc_price = get_binance_price("BTCUSDT")

    if specific_btc_price is not None:
        price_change_percentage = ((current_btc_price - specific_btc_price) / specific_btc_price) * 100
    else:
        price_change_percentage = None

    return render_template('btcprice2.html', bitcoin_price=current_btc_price, change_percentage=price_change_percentage)


