from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError, RequestError
import os
import logging

# Note: Logged errors should be visible in the flask-app logs.
# To view the logs, run the following command from your local host: kubectl logs -l app=flask-app

class ElasticsearchManager:
    def __init__(self):
        # Get Elasticsearch host, user, and password from environment variables
        ES_HOST = os.getenv('ES_HOST')
        ES_USER = os.getenv('ES_USER')
        ES_PASSWORD = os.getenv('ES_PASSWORD')
        # Initialize an Elasticsearch client
        self.es = Elasticsearch(hosts=[ES_HOST], http_auth=(ES_USER, ES_PASSWORD))

    def index_document(self, id, body):
        try:
            # Add or update a document in the 'product_descriptions' index
            self.es.index(index="product_descriptions", id=str(id), body=body)
        except RequestError as e:
            # Log an error if indexing failed
            logging.error(f"Failed to index product in Elasticsearch: {e}")

    def update_document(self, id, body):
        try:
            # Update a document in the 'product_descriptions' index
            self.es.update(index="product_descriptions", id=str(id), body={"doc": body})
        except RequestError as e:
            # Log an error if updating failed
            logging.error(f"Failed to update product in Elasticsearch: {e}")

    def delete_document(self, id):
        try:
            # Check if a document exists in the 'product_descriptions' index
            if self.es.exists(index="product_descriptions", id=str(id)):
                # Delete the document if it exists
                self.es.delete(index="product_descriptions", id=str(id))
        except NotFoundError as e:
            # Log an error if the document was not found
            logging.error(f"Product not found in Elasticsearch: {e}")
        except RequestError as e:
            # Log an error if deleting failed
            logging.error(f"Failed to delete product from Elasticsearch: {e}")

    def search(self, query):
        try:
            # Perform a multi-match search in the 'product_descriptions' index
            response = self.es.search(
                index="product_descriptions",
                body={
                    "query": {
                        "multi_match": {
                            "query": query,
                            "fields": ["description"]
                        }
                    }
                }
            )

            # Parse the search results into a suitable format
            results = [
                {
                    'product_id': hit['_id'],  
                    'product_name': hit['_source']['product_name'],
                    'product_category': hit['_source']['product_category'],
                    'price': hit['_source']['price'],
                    'available_quantity': hit['_source']['available_quantity'],
                    'description': hit['_source']['description']
                }
                for hit in response['hits']['hits']
            ]
            
            return results

        except NotFoundError as e:
            # Log an error if no documents were found
            logging.error(f"Product not found in Elasticsearch: {e}")
        except RequestError as e:
            # Log an error if searching failed
            logging.error(f"Failed to search products in Elasticsearch: {e}")
