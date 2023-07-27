from pymongo import MongoClient
from bson.objectid import ObjectId
import os

class MongoDBManager:
    def __init__(self):
        # Get MongoDB URI from environment variables
        MONGO_URI = os.getenv('MONGO_URI')
        # Initialize a MongoDB client
        client = MongoClient(MONGO_URI)
        # Get a reference to the products database
        self.db = client.products_db
        # Get a reference to the products collection within the database
        self.collection = self.db.products

    def find_all(self):
        # Fetch all products from the collection
        products = self.collection.find()
        return [
            {
                'product_id': str(p['_id']), # Convert ObjectId to string for JSON serialization
                'product_name': p['product_name'],
                'product_category': p['product_category'],
                'price': p['price'],
                'available_quantity': p['available_quantity'],
                'description': p['description']
            }
            for p in products
        ]

    def find_one(self, product_id):
        # Find a single product by its ID
        product = self.collection.find_one({'_id': ObjectId(product_id)})
        # Return the product data if found, otherwise return None
        if product:
            return {
                'product_id': str(product['_id']), # Convert ObjectId to string for JSON serialization
                'product_name': product['product_name'], 
                'product_category': product['product_category'], 
                'price': product['price'], 
                'available_quantity': product['available_quantity'],
                'description': product['description']
                }
        return None

    def create(self, product_data):
        # Insert a new product into the collection and get its ID
        product_id = self.collection.insert_one(product_data).inserted_id
        # Fetch the newly created product data from the database and return it
        return self.find_one(str(product_id)) # Convert ObjectId to string for JSON serialization

    def update(self, product_id, product_data):
        # Update a specific product in the collection
        self.collection.update_one({'_id': ObjectId(product_id)}, {'$set': product_data})
        # Fetch the updated product data from the database and return it
        return self.find_one(str(product_id)) # Convert ObjectId to string for JSON serialization

    def delete(self, product_id):
        # Delete a specific product from the collection
        result = self.collection.delete_one({'_id': ObjectId(product_id)})
        # Return True if a product was deleted, False otherwise
        return result.deleted_count > 0

    def analytics(self):
        # Define a pipeline for aggregation
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
