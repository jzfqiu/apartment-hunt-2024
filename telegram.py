import os
import re

import requests


bot_api_token = os.environ.get("TELEGRAM_BOT_TOKEN")
my_chat_id = os.environ.get("TELEGRAM_MY_CHAT_ID")


base_url = f"https://api.telegram.org/bot{bot_api_token}"

def send_message(msg: str) -> None:
    data = {
        "chat_id": my_chat_id,
        "parse_mode": "MarkdownV2",
        "text": re.sub(r"([#$-])", lambda match: "\\" + match.group(0), msg),
    }
    response = requests.post(f"{base_url}/sendMessage", json=data)
    try:
        response.raise_for_status()
    except requests.HTTPError:
        print(response.text)
