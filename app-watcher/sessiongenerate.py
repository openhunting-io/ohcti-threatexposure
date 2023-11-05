from telethon.sync import TelegramClient
from telethon.tl.types import Document
from telethon.errors import TimedOutError
import os
import time
import json

# Replace these values with your own API ID, API hash, and phone number.
api_id = os.environ.get('TELEGRAM_API_ID')
api_hash = os.environ.get('TELEGRAM_API_HASH')
phone_number = os.environ.get('TELEGRAM_PHONE_NUMBER')

with TelegramClient(phone_number, api_id, api_hash) as client:
    # Start a session for the client
    client.start()
    print("Telegram Successfull Login, now you can close this!")