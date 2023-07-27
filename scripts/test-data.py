from pymongo import MongoClient
from random import choice, randint
from faker import Faker
import requests


fake = Faker()

MONGO_URI = 'mongodb://127.0.0.1:27017/products_db' # MongoDB URI
client = MongoClient(MONGO_URI) # Create a MongoDB client
db = client.products_db # Create a database called products_db
collection = db.products # Create a collection called products

# list of sample product names
product_names = ['Product A', 'Product B', 'Product C', 'Product D']

# list of sample product categories
product_categories = ['Category 1', 'Category 2', 'Category 3', 'Category 4']

# Create 100 sample products
for _ in range(100):
    product_description = fake.text(max_nb_chars=200)  # generates random words of up to 200 characters
    product_data = {
        'product_name': choice(product_names),
        'product_category': choice(product_categories),
        'price': randint(10, 100),  # random price between 10 and 100
        'available_quantity': randint(1, 20),  # random quantity between 1 and 20
        'description': product_description,
    }
    response = requests.post('http://localhost:5000/products', json=product_data)

    if response.status_code != 201:
        print(f"Failed to post product: {response.text}")

print("Test data created successfully.")
