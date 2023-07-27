from flask import Flask, request, jsonify, render_template
from marshmallow import ValidationError
from repositories import ProductRepository
from models import Product
from product_schema import ProductSchema
import os
from bson.errors import InvalidId


# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')

# Initialize product schema for validation with marshmallow
product_schema = ProductSchema()

# Initialize product repository
product_repo = ProductRepository()

# Define route for retrieving all products
@app.route('/products', methods=['GET']) 
def get_products():
    try:
        products = product_repo.find_all()
        return jsonify(products), 200
    except ValueError as ve: # ValueError is raised when the product analytics fails
        return jsonify({'error': str(ve)}), 404

# Define route for retrieving a specific product by ID
@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = product_repo.find_one(product_id)
        if product:
            return jsonify({'result': product}), 200
    except InvalidId: # bson.errors.InvalidId is raised when the product_id is not a valid ObjectId
        return jsonify({'error': 'Invalid product ID'}), 400
    return jsonify({'error': 'Product not found'}), 404 

# Define route for adding a product
@app.route('/products', methods=['POST'])
def add_product():
    try:
        # Validate and deserialize input data
        product_data = product_schema.load(request.get_json()) 
        new_product = product_repo.create(Product(product_data)) 
        if new_product: 
            return jsonify({'result': new_product}), 201
    except ValidationError as err: # marshmallow.exceptions.ValidationError is raised when the input data is invalid
        return jsonify(err.messages), 400
    except ValueError as ve: # ValueError is raised when the product creation fails
        return jsonify({'error': str(ve)}), 500
    return jsonify({'error': 'Failed to create product'}), 500

# Define route for updating a product
@app.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        # Validate and deserialize input data
        product_data = product_schema.load(request.get_json())
        updated_product = product_repo.update(product_id, Product(product_data))
        if updated_product:
            return jsonify({'result': updated_product}), 200
    except InvalidId: # bson.errors.InvalidId is raised when the product_id is not a valid ObjectId
        return jsonify({'error': 'Invalid product ID'}), 400
    except ValidationError as err: # marshmallow.exceptions.ValidationError is raised when the input data is invalid
        return jsonify(err.messages), 400
    return jsonify({'error': 'Product not found'}), 404

# Define route for deleting a product
@app.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        deleted_product = product_repo.delete(product_id)
        if deleted_product:
            return jsonify({'result': 'Product deleted successfully.'}), 200
    except InvalidId: # bson.errors.InvalidId is raised when the product_id is not a valid ObjectId
        return jsonify({'error': 'Invalid product ID'}), 400
    return jsonify({'error': 'Product not found'}), 404

# Define route for searching products
@app.route('/products/search', methods=['GET'])
def search_products():
    try:
        query = request.args.get("query")
        results = product_repo.search(query)
        return jsonify(results), 200
    except ValueError as ve: # ValueError is raised when the product search fails
        return jsonify({'error': str(ve)}), 404

# Define route for retrieving product analytics
@app.route('/products/analytics', methods=['GET'])
def get_product_analytics():
    try:
        analytics = product_repo.analytics()
        return jsonify(analytics), 200
    except ValueError as ve: # ValueError is raised when the product analytics fails
        return jsonify({'error': str(ve)}), 404
    
# Define route for the index page
@app.route('/', methods=['GET'])
def index(): 
    return render_template('index.html') 

# Define route for the add product page
@app.route('/add_product', methods=['GET'])
def add_product_page():
    return render_template('add_product.html')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('FLASK_DEBUG')) 
