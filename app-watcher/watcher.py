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

channel_file_path = '/channel/telegram.txt'
record_file = 'downloaded_files.json'

# Function to read the list of channels from the file
def read_channels():
    with open(channel_file_path, 'r') as channel_file:
        return channel_file.read().splitlines()

# Initialize the list of channels
channels = read_channels()
previous_channels = set(channels)

# Create a dictionary to store processed file names for each channel
processed_files = {channel: set() for channel in channels}

# Function to save the list of processed files to a JSON record
def save_processed_files():
    with open(record_file, 'w') as record:
        json.dump({channel: list(processed_files[channel]) for channel in channels}, record)

# Load the record of downloaded files, or initialize an empty dictionary if the file is empty or not valid JSON
if os.path.isfile(record_file):
    with open(record_file, 'r') as file:
        try:
            downloaded_record = json.load(file)
        except json.JSONDecodeError:
            downloaded_record = {}
        for channel, downloaded_files in downloaded_record.items():
            processed_files[channel] = set(downloaded_files)

with TelegramClient(phone_number, api_id, api_hash) as client:
    # Start a session for the client
    client.start()

    # Create a directory to save downloaded files
    download_directory = '/breachfiles/'

    last_mtime = os.path.getmtime(channel_file_path)

    while True:
        # Check for changes in the channel file
        current_mtime = os.path.getmtime(channel_file_path)
        if current_mtime != last_mtime:
            last_mtime = current_mtime
            updated_channels = set(read_channels())

            # Print added channels
            added_channels = updated_channels - previous_channels
            if added_channels:
                print("Added channels:", ", ".join(added_channels))

            # Print removed channels
            removed_channels = previous_channels - updated_channels
            if removed_channels:
                print("Removed channels:", ", ".join(removed_channels))

            # Update the processed files dictionary
            channels = updated_channels
            previous_channels = updated_channels
            for channel in channels:
                if channel not in processed_files:
                    processed_files[channel] = set()

        # Continuously check for new messages in specified channels
        for channel in channels:
            try:
                for message in client.iter_messages(channel):
                    if message.document and isinstance(message.document, Document) and message.document.mime_type == 'text/plain':
                        # Check if the message contains a document and is of type text/plain
                        file_name = message.file.name
                        if file_name not in processed_files[channel]:
                            file_path = client.download_media(message, file=download_directory)
                            print(f'Downloaded: {file_name}')
                            processed_files[channel].add(file_name)
                            save_processed_files()  # Save the updated record of downloaded files
            except TimedOutError as e:
                print("Timed out. Retrying...")
                time.sleep(5)  # Add a delay and then retry the request.
