# Inventory Management System - IMS-DEMO

This is a demo inventory management system built with Flask. The application uses MongoDB for data storage, Elasticsearch for full-text search, and it's containerized with Docker and can be deployed on Minikube.

## Objective

The system includes:

- CRUD operations for managing the product inventory.
- Full-text search for products based on their descriptions using Elasticsearch.
- Aggregated product metrics such as the most popular product categories or average price of products.

## Prerequisites

This setup has been tested on a Windows environment. Before you start, make sure you have the following installed on your machine:

- Docker
- Minikube
- kubectl
- Python 3.6+

## Pull the Repository

Use Git to clone the repository:

```bash
git clone https://github.com/koryehoffman/ims-demo.git
```

## Deployment Steps

Follow these steps to deploy the application:

1. Start Minikube: 
    ```
    minikube start
    ```

2. Navigate to the `scripts` directory and run the `deploy.ps1` script: 
    ```
    cd scripts
    powershell -ExecutionPolicy Bypass -File .\deploy.ps1
    ```

    The `deploy.ps1` script performs the following tasks:

    - Sets Docker to use the Minikube Docker daemon.
    - Builds a Docker image for the Flask application.
    - Applies Kubernetes configurations for Elasticsearch, Flask app, and MongoDB.
    - Waits until the Flask app pod is in the 'Running' state.
    - Forwards the port for the Flask service to be accessible from localhost.

    Once the script execution is complete, the Flask app should be accessible at `http://localhost:5000`. There is a very basic UI available if you navigate to this url via a browser, however this demo is currently
    inteded to be used via API. The UI is only an initial test of a couple features but may be expanded upon.

    Next you will want to run the test-data.py script using the command below. Optionally you may edit the script to modify the test data that is loaded into the DB.
    ````
    python .\test-data.py
    ````

3. Test the API endpoints

    For simplicity, I have also included a Postman collection which you can import.
    Note: To run the elasticsearch commands from your local machine, you must also run the command below from a terminal.
    Additionally included is the command for mongodb should you wish to connect it to it from your localhost.
    ````
    kubectl port-forward service/elasticsearch-service 9200:9200
    kubectl port-forward service/mongodb-service 27017:27017
    ````

## API Endpoints

The REST API includes the following endpoints:

- `GET /products`: List all products
- `GET /products/{id}`: Fetch a specific product
- `POST /products`: Add a new product
- `PUT /products/{id}`: Update an existing product  
- `DELETE /products/{id}`: Delete a product
- `GET /products/search?query={keywords}`: Fetch products whose descriptions match the specified keywords
- `GET /products/analytics`: Fetch aggregated product data, such as the total count of products, the most popular product category, and the average price of products

## Project Structure

- `flask-app`: Contains the main Flask application and its Dockerfile along with its K8 config files.
- `elasticsearch-app` and `mongodb-app`: Contains the K8 configurations for Elasticsearch and MongoDB.
- `configs`: Contains the environment configuration for the application.
- `scripts`: Contains the deployment script and a Python script for generating test data.

## Note

This system is designed for demonstration purposes. For a production environment, more security measures would be necessary, like traffic encryption and secure handling of secrets.

For any issues, please create a new issue in the repo.
