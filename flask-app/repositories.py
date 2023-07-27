from MongoDBManager import MongoDBManager
from ElasticsearchManager import ElasticsearchManager

class ProductRepository:
    # Initialize managers for MongoDB and Elasticsearch
    mongo_manager = MongoDBManager()
    es_manager = ElasticsearchManager()

    # Function to retrieve all products from the MongoDB
    def find_all(self):
        result = self.mongo_manager.find_all()
        return result

    # Function to retrieve a specific product from the MongoDB using its product_id
    def find_one(self, product_id):
        result = self.mongo_manager.find_one(product_id)
        return result

    # Function to create a new product in the MongoDB and index it in Elasticsearch
    def create(self, product):
        result = None
        try:
            # Create product in MongoDB
            result = self.mongo_manager.create(product.product_data)
            product_id = result['product_id']
            # Remove the _id field as it's an ObjectId and not JSON serializable
            product.product_data.pop('_id')  
            # Index the product data in Elasticsearch
            self.es_manager.index_document(product_id, product.product_data)
            return result
        except Exception as e:
            # If there was a problem, delete the product from MongoDB and re-raise the exception
            if result:
                self.mongo_manager.delete(product_id)
            raise

    # Function to update a specific product in the MongoDB and re-index it in Elasticsearch
    def update(self, product_id, product):
        result = None
        try:
            # Get the original product data
            original_product_data = self.mongo_manager.find_one(product_id)
            # Update the product data in MongoDB
            result = self.mongo_manager.update(product_id, product.product_data)
            # Index the updated product data in Elasticsearch
            self.es_manager.index_document(product_id, product.product_data)
            return result
        except Exception as e:
            # If there was a problem, revert to the original product data in MongoDB and re-raise the exception
            if result:
                self.mongo_manager.update(product_id, original_product_data)
            raise

    # Function to delete a specific product from the MongoDB and remove its index from Elasticsearch
    def delete(self, product_id):
        result = None
        try:
            # Get the original product data
            original_product_data = self.mongo_manager.find_one(product_id)
            # Delete the product from MongoDB
            result = self.mongo_manager.delete(product_id)
            # Delete the product index from Elasticsearch
            self.es_manager.delete_document(product_id)
            return result
        except Exception as e:
            # If there was a problem, re-create the original product data in MongoDB and re-raise the exception
            if result:
                self.mongo_manager.create(original_product_data)
            raise

    # Function to search for products in Elasticsearch using a query string
    def search(self, query):
        results = self.es_manager.search(query)
        return results

    # Function to get analytics about the products from MongoDB
    def analytics(self):
        results = self.mongo_manager.analytics()
        return results
