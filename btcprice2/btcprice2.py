import requests
import json
import time
from telegram import Bot
import asyncio
from flask import Flask, render_template  # Thêm Flask và render_template

app = Flask(__name__)

# Thay thế YOUR_BOT_TOKEN và YOUR_CHAT_ID bằng thông tin của bot Telegram của bạn
bot = Bot(token="6163331718:AAG7J467TQi53Xie1b9nAnnRP4sbJmlhiOY")
chat_id = "974909109"

def get_binance_price(symbol="BTCUSDT"):
    base_url = "https://api.binance.com/api/v3/ticker/price"
    params = {"symbol": symbol}
    
    try:
        response = requests.get(base_url, params=params)
        data = json.loads(response.text)
        return float(data["price"])
    except Exception as e:
        print(f"Lỗi khi lấy giá: {e}")
        return None

# Tạo một route để hiển thị thông tin giá Bitcoin trên trang web
@app.route('/')
def display_bitcoin_price():
    bitcoin_price = get_binance_price()
    return render_template('btcprice2.html', bitcoin_price=bitcoin_price)
# Tạo một route để trả về giá Bitcoin dưới dạng JSON
@app.route('/get_bitcoin_price')
def get_bitcoin_price_json():
    bitcoin_price = get_binance_price()
    return {'bitcoin_price': bitcoin_price}


async def main():
    symbol = "BTCUSDT"  # Mã giao dịch BTC/USDT
    while True:
        bitcoin_price = get_binance_price(symbol)
        if bitcoin_price is not None:
            message = f"Giá Bitcoin (BTC/USDT): {bitcoin_price} USDT"
            print(message)  # In thông báo vào console
            await bot.send_message(chat_id=chat_id, text=message)  # Gửi thông báo trên Telegram
        time.sleep(1)  # Giá này nhìn nhiều sẽ bị say sóng :)))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())  # Tạo một task asyncio cho hàm main()
    
    # Chạy Flask trong luồng chính của chương trình
    app.run(debug=True)
