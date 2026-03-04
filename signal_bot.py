import requests
from datetime import datetime, timedelta
import os

TINKOFF_TOKEN = os.environ.get('TINKOFF_TOKEN')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

INSTRUMENTS = {
    "Сургутнефтегаз": {"figi": "BBG0047310Y3", "level": 22.5},
    "Лукойл": {"figi": "BBG004731032", "level": 5500.0},
    "Газпром": {"figi": "BBG004730RP0", "level": 128.0},
    "МТС": {"figi": "BBG004730Y88", "level": 230.0},
}

TINKOFF_API_URL = "https://api-invest.tinkoff.ru/openapi/v1/market/candles"

def get_current_price(figi):
    headers = {"Authorization": f"Bearer {TINKOFF_TOKEN}"}
    end = datetime.now()
    start = end - timedelta(minutes=5)
    params = {
        "figi": figi,
        "from": start.isoformat() + "Z",
        "to": end.isoformat() + "Z",
        "interval": "1min"
    }
    try:
        r = requests.get(TINKOFF_API_URL, headers=headers, params=params, timeout=10)
        data = r.json()
        if data.get("payload", {}).get("candles"):
            last_candle = data["payload"]["candles"][-1]
            return float(last_candle["c"])
    except Exception as e:
        print(f"Ошибка: {e}")
    return None

def check_signal(price, level):
    if price is None:
        return False
    return abs(price - level) / level < 0.002

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data, timeout=10)
        print(f"Отправлено: {message}")
    except Exception as e:
        print(f"Ошибка: {e}")

def main():
    print(f"Проверка цен в {datetime.now().strftime('%H:%M:%S')}")
    for name, data in INSTRUMENTS.items():
        price = get_current_price(data["figi"])
        if check_signal(price, data["level"]):
            msg = (f"🔔 {name}\nУровень: {data['level']}\nЦена: {price:.2f}\nВремя: {datetime.now().strftime('%H:%M')}")
            send_telegram(msg)
        else:
            print(f"{name}: {price if price else 'нет данных'}")

if __name__ == "__main__":
    main()