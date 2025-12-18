import os
import sys
import urllib.parse
import requests

def send_message(token: str, chat_id: str, text: str) -> None:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    resp = requests.post(url, data={"chat_id": chat_id, "text": text})
    data = resp.json()

    if not data.get("ok"):
        raise RuntimeError(f"Telegram API error: {data}")

def main():
    # 1) берём токен и chat_id из переменных окружения
    token = os.getenv("TG_BOT_TOKEN")
    chat_id = os.getenv("TG_CHAT_ID")

    if not token or not chat_id:
        print("❌ Не заданы переменные окружения TG_BOT_TOKEN и/или TG_CHAT_ID")
        print("Пример (PowerShell):")
        print('$env:TG_BOT_TOKEN="123:ABC"')
        print('$env:TG_CHAT_ID="-1001234567890"')
        sys.exit(1)

    # 2) файл из аргумента
    if len(sys.argv) != 2:
        print("Usage: python tg_send.py message.txt")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print("❌ Файл пустой")
        sys.exit(1)

    send_message(token, chat_id, text)
    print("✅ Message sent to Telegram")

if __name__ == "__main__":
    main()
