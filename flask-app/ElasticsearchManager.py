from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError, RequestError
import os

class ElasticsearchManager:
    def __init__(self, index):
        # Get Elasticsearch host, user, and password from environment variables
        ES_HOST = os.getenv('ES_HOST')
        ES_USER = os.getenv('ES_USER')
        ES_PASSWORD = os.getenv('ES_PASSWORD')

        # Initialize an Elasticsearch client
        self.es = Elasticsearch(hosts=[ES_HOST], http_auth=(ES_USER, ES_PASSWORD))
        self.index_name = index

    def index_document(self, id, body):
        try:
            body_copy = body.copy() # Create a copy of the body to avoid modifying the original
            body_copy.pop('_id', None) # Remove the '_id' field from the body copy
            # Add or update a document in the specified index
            self.es.index(index=self.index_name, id=id, body=body_copy)
        except RequestError as e:
            # Raise an error if indexing failed
            raise(f"Failed to update ${self.index_name} in Elasticsearch: {e}")

    def update_document(self, id, body):
        try:
            body_copy = body.copy() # Create a copy of the body to avoid modifying the original
            body_copy.pop('_id', None) # Remove the '_id' field from the body copy
            # Update a document in the specified index
            self.es.update(index=self.index_name, id=id, body={"doc": body_copy})
        except RequestError as e:
            # Raise an error if updating failed
            raise(f"Failed to update ${self.index_name} in Elasticsearch: {e}")

    def delete_document(self, id):
        try:
            # Check if a document exists in the specified index
            if self.es.exists(index=self.index_name, id=id):
                # Delete the document if it exists
                self.es.delete(index=self.index_name, id=id)
        except NotFoundError as e:
            # Raise an error if the document was not found
            raise(f"Not found in ${self.index_name} Elasticsearch: {e}")
        except RequestError as e:
            # Raise an error if deleting failed
            raise(f"Failed to delete from ${self.index_name} from Elasticsearch: {e}")

    def search(self, query):
        try:
            # Perform a multi-match search by description in the specified index
            # At present this could be a match instead of multi-match, though I'm leaving it as multi-match in case we want to add more fields to search by in the future.
            # Would like to include product_name with heavier weights, but additional changes would need to be made to keep the function generic. May be worth it in the future.
            response = self.es.search(
                index=self.index_name,
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
            results = []
            for hit in response['hits']['hits']:
                hit['_source']['_id'] = hit['_id']
                results.append(hit['_source'])
            
            return results

        except NotFoundError as e:
            # Raise an error if no documents were found
            raise(f"Not found in ${self.index_name} from Elasticsearch: {e}")
        except RequestError as e:
            # Raise an error if searching failed
            raise(f"Failed to search in ${self.index_name} from Elasticsearch: {e}")
