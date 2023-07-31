from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import json
from json_encoder import JSONEncoder

class MongoDBManager:
    def __init__(self, db_name, collection_name):
        # Get MongoDB URI from environment variables
        MONGO_URI = os.getenv('MONGO_URI')

        # Initialize a MongoDB client
        client = MongoClient(MONGO_URI)
        self.db = client[db_name] # Get a reference to the sepcified database
        self.collection = self.db[collection_name] # Get a reference to the specified collection within the database

    def find_all(self):
        docs = list(self.collection.find()) # Fetch all documents from the collection
        json_docs = JSONEncoder().encode(docs) # Serialize the documents to JSON using the custom JSON Encoder
        result = json.loads(json_docs) # Parse the JSON string back to a Python list of dictionaries
        return result
    
    def find_one(self, id):
        # Find a single document by its ID
        doc = self.collection.find_one({'_id': ObjectId(id)})
        if doc:
            # Serialize the document to JSON
            json_doc = JSONEncoder().encode(doc) # Serialize the document to JSON using the custom JSON Encoder
            result = json.loads(json_doc) # Parse the JSON string back to a Python dictionary
            return result
        return None

    def create(self, data):
        # Insert a new document into the collection and get its ID
        id = self.collection.insert_one(data).inserted_id
        # Fetch the newly created document from the database and return it
        result = self.find_one(id)
        return result

    def update(self, id, data):
        # Update a specific document in the collection
        self.collection.update_one({'_id': ObjectId(id)}, {'$set': data})
        # Fetch the updated document from the database and return it
        result = self.find_one(id)
        return result

    def delete(self, id):
        # Delete a specific document from the collection
        result = self.collection.delete_one({'_id': ObjectId(id)})
        # Return True if a document was deleted, False otherwise
        return result.deleted_count > 0

    def product_analytics(self):
        # Define the pipeline for aggregation
        pipeline = [
            {"$group": {
                "_id": "$product_category",
                "averagePrice": {"$avg": "$price"},
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}}
        ]
        # Execute the aggregation pipeline
        results = list(self.collection.aggregate(pipeline))
        if results:
            most_common_category = results[0]["_id"]
            avg_price_most_common_category = results[0]["averagePrice"]
        else:
            most_common_category = None
            avg_price_most_common_category = None

        # Get the total number of products
        total_products = self.collection.count_documents({})

        # Return the analytics data
        return {
            "total_products": total_products,
            "most_common_category": most_common_category,
            "avg_price_most_common_category": avg_price_most_common_category
        }
