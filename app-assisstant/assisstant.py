import os
import requests
import time
from elasticsearch import Elasticsearch

# Load environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Define the base URL for the Telegram Bot API
API_BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'

# Store the last update ID to avoid processing the same update multiple times
last_update_id = None

# Define the Elasticsearch client with the host URL (including scheme) and port
es = Elasticsearch(hosts=['http://elasticsearch:9200'], verify_certs=False)

def send_message(chat_id, text):
    url = API_BASE_URL + 'sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=data)
    return response.json()

def get_updates():
    url = API_BASE_URL + 'getUpdates'
    params = {'offset': last_update_id + 1 if last_update_id else None, 'timeout': 30}
    response = requests.get(url, params=params)
    return response.json()

while True:
    updates = get_updates()
    if updates['result']:
        for update in updates['result']:
            last_update_id = update['update_id']
            chat_id = update['message']['chat']['id']
            message_text = update['message']['text']
            
            # Process the message and prepare a response
            if message_text.startswith('/search'):
                # Extract the search query from the message
                search_query = message_text[len('/search '):]

                # Escape any special characters in the search query
                search_query = search_query.replace('/', '\\/')

                # Define the dynamic search query using the "wildcard" query
                es_query = {
                    "query": {
                        "wildcard": {
                            "message": f"*{search_query}*"
                        }
                    },
                    "size": 1000
                }


                # Perform the search
                results = es.search(index="ctionbudget-unamepass", body=es_query)

                # Extract and format the search results
                response_text = "Search Results:\n"
                for hit in results['hits']['hits']:
                    message = hit['_source']['message']
                    response_text += f"- {message}\n"

                if not results['hits']['hits']:
                    response_text = "No results found."

                # Send the search results as a response to the chat
                send_message(chat_id, response_text)

    # Delay to avoid excessive API calls
    time.sleep(1)
