from telethon.sync import TelegramClient
from telethon.tl.types import Document, Channel, Chat
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

# Function to read the list of channels and groups from the file
def read_channels_and_groups():
    with open(channel_file_path, 'r') as channel_file:
        return channel_file.read().splitlines()

# Initialize the list of channels and groups
channels_and_groups = read_channels_and_groups()
previous_channels_and_groups = set(channels_and_groups)

# Create a dictionary to store processed file names for each channel or group
processed_files = {channel_or_group: set() for channel_or_group in channels_and_groups}

# Function to save the list of processed files to a JSON record
def save_processed_files():
    with open(record_file, 'w') as record:
        json.dump({channel_or_group: list(processed_files[channel_or_group]) for channel_or_group in channels_and_groups}, record)

# Load the record of downloaded files, or initialize an empty dictionary if the file is empty or not valid JSON
if os.path.isfile(record_file):
    with open(record_file, 'r') as file:
        try:
            downloaded_record = json.load(file)
        except json.JSONDecodeError:
            downloaded_record = {}
        for channel_or_group, downloaded_files in downloaded_record.items():
            processed_files[channel_or_group] = set(downloaded_files)

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
            updated_channels_and_groups = set(read_channels_and_groups())

            # Print added channels and groups
            added_channels_and_groups = updated_channels_and_groups - previous_channels_and_groups
            if added_channels_and_groups:
                print("Added channels and groups:", ", ".join(added_channels_and_groups))

            # Print removed channels and groups
            removed_channels_and_groups = previous_channels_and_groups - updated_channels_and_groups
            if removed_channels_and_groups:
                print("Removed channels and groups:", ", ".join(removed_channels_and_groups))

            # Update the processed files dictionary
            channels_and_groups = updated_channels_and_groups
            previous_channels_and_groups = updated_channels_and_groups
            for channel_or_group in channels_and_groups:
                if channel_or_group not in processed_files:
                    processed_files[channel_or_group] = set()

        # Continuously check for new messages in specified channels and groups
        for channel_or_group in channels_and_groups:
            try:
                entity = client.get_entity(channel_or_group)
                if isinstance(entity, Channel):
                    # It's a channel
                    messages = client.iter_messages(entity)
                elif isinstance(entity, Chat):
                    # It's a group
                    messages = client.iter_messages(channel_or_group)
                else:
                    continue  # Skip if it's neither a channel nor a group

                for message in messages:
                    if message.document and isinstance(message.document, Document) and message.document.mime_type == 'text/plain':
                        # Check if the message contains a document and is of type text/plain
                        file_name = message.file.name
                        if file_name not in processed_files[channel_or_group]:
                            file_path = client.download_media(message, file=download_directory)
                            print(f'Downloaded: {file_name}')
                            processed_files[channel_or_group].add(file_name)
                            save_processed_files()  # Save the updated record of downloaded files
            except TimedOutError as e:
                print("Timed out. Retrying...")
                time.sleep(5)  # Add a delay and then retry the request.
