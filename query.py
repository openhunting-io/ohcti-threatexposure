from elasticsearch import Elasticsearch

# Define the Elasticsearch client with the host URL (including scheme) and port
es = Elasticsearch(hosts=['http://localhost:9200'], verify_certs=False)

# Get the user input for the search text
search_text = input("Enter the search text: ")

# Escape any special characters in the search text
search_text = search_text.replace('/', '\\/')

# Define the dynamic search query using the "wildcard" query
search_query = {
    "query": {
        "wildcard": {
            "message": f"*{search_text}*"
        }
    }
}

# Perform the search with the correct 'Content-Type' header
results = es.search(index="ctionbudget-unamepass", body=search_query)

# Extract and print the "message" field from the hits
for hit in results['hits']['hits']:
    message = hit['_source']['message']
    print(message)

# Close the Elasticsearch client when you're done
es.close()
