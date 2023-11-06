import os
import requests
import time
from elasticsearch import Elasticsearch
import re
from collections import defaultdict

# Load environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')

if BOT_TOKEN is None:
    raise ValueError("BOT_TOKEN environment variable is not set")

# Define the base URL for the Telegram Bot API
API_BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'

# Store the last update ID to avoid processing the same update multiple times
last_update_id = None


# Define the Elasticsearch client with the host URL (including scheme) and port
es = Elasticsearch(hosts=['http://elasticsearch:9200'], verify_certs=False, request_timeout=120)

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
    try:
        updates = get_updates()
        if 'result' in updates and updates['result']:
            for update in updates['result']:
                last_update_id = update['update_id']
                chat_id = update['message']['chat']['id']
                message_text = update['message']['text']
                
                if len(message_text.replace("/search","").replace("/map","")) < 8:
                    send_message(chat_id, "Command is too short")
                    continue

                # Process the message and prepare a response
                if message_text.startswith('/search'):
                    # Extract the search query from the message
                    search_query = message_text[len('/search '):]
                    
                    search_query = search_query.lower()
                    

                    # Escape any special characters in the search query
                    search_query = search_query.replace('/', '\\/')
                    
                    # Define the dynamic search query using the "wildcard" query
                    es_query = {
                        "query": {
                            "wildcard": {
                                "message": f"*{search_query}*"
                            }
                        },
                        "size": 10000
                    }
                    try:
                        send_message(chat_id, "Start Searching")
                        # Perform the search with the correct 'Content-Type' header
                        results = es.search(index="ctionbudget-unamepass", body=es_query)

                        # Initialize a dictionary to group URLs by subdomain
                        url_groups = defaultdict(list)

                        # Define a regular expression pattern to extract information
                        pattern = r'https?://([^/:]+)(?::|;| )(.*?)(?::|;| )(.*)'
                        
                        # Process the Elasticsearch search results
                        for hit in results['hits']['hits']:
                            message = hit['_source']['message']
                            match = re.match(pattern, message)
                            if match:
                                subdomain, username, password = match.groups()
                                url = f"https://{subdomain}"
                                url_groups[subdomain].append(f"{url} {username}:{password}")

                        # Send messages for each subdomain batch
                        for subdomain, urls in url_groups.items():
                            response_text = f"Subdomain: {subdomain}\n\n"
                            max_batch_size = 10  # Define the maximum number of URLs per batch

                            # Slice the URLs into batches
                            for i in range(0, len(urls), max_batch_size):
                                batch = urls[i:i + max_batch_size]
                                for url in batch:
                                    response_text += f"{url}\n"

                                # Send the message to Telegram (replace with your actual Telegram sending code)
                                send_message(chat_id, response_text)
                        send_message(chat_id, "End of Message")
                    except Exception as e:
                        print(f"An error occurred: {e}")
                elif message_text.startswith('/map'):
                    search_query = message_text[len('/map '):]
                    
                    search_query = search_query.lower()
                    
                    # Escape any special characters in the search query
                    search_query = search_query.replace('/', '\\/')
                    
                    # Define the dynamic search query using the "wildcard" query
                    es_query = {
                        "query": {
                            "wildcard": {
                                "message": f"*{search_query}*"
                            }
                        },
                        "size": 10000
                    }
                    
                    try:
                        send_message(chat_id, "Start Mapping")
                        # Perform the search with the correct 'Content-Type' header
                        results = es.search(index="ctionbudget-unamepass", body=es_query)

                        # Initialize a dictionary to group URLs by subdomain
                        url_groups = defaultdict(list)
                        subdomains = set()

                        # Define a regular expression pattern to extract information
                        pattern = r'https?://([^/:]+)(?::|;| )(.*?)(?::|;| )(.*)'
                        
                        # Process the Elasticsearch search results
                        for hit in results['hits']['hits']:
                            message = hit['_source']['message']
                            match = re.search(pattern, message)
                            if match:
                                subdomain = match.group(1)
                                subdomains.add(subdomain)

                        # Create a list of "/search" commands for subdomains
                        search_commands = [f"{subdomain}" for subdomain in subdomains]
                        # Send the list of search commands as a single message
                        response_text = "Subdomains to search:\n" + "\n".join(search_commands)
                        send_message(chat_id, response_text)
                        send_message(chat_id, "End of Message")
                    except Exception as e:
                        print(f"An error occurred: {e}")
                else:
                    send_message(chat_id, "Use /search or /map")
                    

        # Delay to avoid excessive API calls
        time.sleep(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # Introduce a delay when an exception occurs
        time.sleep(5)
