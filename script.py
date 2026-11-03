import requests
import os
import time
from dotenv import load_dotenv

load_dotenv(".env")

TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN não encontrado no .env")

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def updates(offset=None):
    response = requests.get(
        f"{BASE_URL}/getUpdates",
        params={
            "offset": offset,
            "timeout": 30
        },
        timeout=35
    )

    response.raise_for_status()
    data = response.json()

    if not data["ok"]:
        raise RuntimeError(data)

    return data["result"]


def send_message(chat_id, message):
    response = requests.post(
        f"{BASE_URL}/sendMessage",
        data={
            "chat_id": chat_id,
            "text": message
        },
        timeout=10
    )

    response.raise_for_status()
    return response.json()


last_update_id = None

while True:
    try:
        received_updates = updates(
            offset=last_update_id + 1 if last_update_id is not None else None
        )

        for update in received_updates:
            last_update_id = update["update_id"]

            message = update.get("message")

            if not message or "text" not in message:
                continue

            chat_id = message["chat"]["id"]
            text = message["text"]

            print(f"Mensagem recebida: {text}")

            send_message(chat_id, "Olá, tudo bem?")

    except requests.RequestException as e:
        print(f"Erro de conexão: {e}")
        time.sleep(3)

    except Exception as e:
        print(f"Erro: {e}")
        time.sleep(3)