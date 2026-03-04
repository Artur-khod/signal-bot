import requests
from datetime import datetime, timedelta
import os

TINKOFF_TOKEN = os.environ.get('TINKOFF_TOKEN')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

print("=== ПРОВЕРКА СОЕДИНЕНИЯ ===")
print(f"Токен Тинькофф: {'✅ есть' if TINKOFF_TOKEN else '❌ нет'}")
print(f"Токен бота: {'✅ есть' if TELEGRAM_BOT_TOKEN else '❌ нет'}")
print(f"ID канала: {'✅ есть' if TELEGRAM_CHAT_ID else '❌ нет'}")

# Проверяем соединение с API Тинькофф
url = "https://api-invest.tinkoff.ru/openapi/sandbox/v1/market/candles"
figi = "BBG0047310Y3"  # Сургутнефтегаз
end = datetime.now()
start = end - timedelta(minutes=5)
params = {
    "figi": figi,
    "from": start.isoformat() + "Z",
    "to": end.isoformat() + "Z",
    "interval": "1min"
}
headers = {"Authorization": f"Bearer {TINKOFF_TOKEN}"}

try:
    print(f"Отправляю запрос к API Тинькофф...")
    r = requests.get(url, headers=headers, params=params, timeout=10)
    print(f"Статус ответа: {r.status_code}")
    print(f"Ответ: {r.text[:200]}")
except Exception as e:
    print(f"Ошибка: {e}")

# Проверяем отправку в Telegram
try:
    test_msg = f"✅ Тест от {datetime.now().strftime('%H:%M:%S')}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": test_msg}
    r = requests.post(url, data=data, timeout=10)
    if r.status_code == 200:
        print("✅ Сообщение в Telegram отправлено")
    else:
        print(f"❌ Ошибка Telegram: {r.status_code}")
except Exception as e:
    print(f"❌ Ошибка отправки в Telegram: {e}")
