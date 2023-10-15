require('dotenv').config();
const axios = require("axios");

// Define the base URL for the Flask service
const baseURL = process.env.FLASK_URI;

const resolvers = {
    // Resolvers for queries
    Query: {
        // Fetch a list of all products
        products: async (root, args, context, info) => {
            try {
                const response = await axios.get(`${baseURL}/products`);
                return response.data;
            } catch (error) {
                handleError(error);
            }
        },

        // Fetch a single product by its _id
        product: async (root, args, context, info) => {
            const { _id } = args;  // Destructure _id from arguments
            try {
                const response = await axios.get(`${baseURL}/products/${_id}`);
                return response.data;
            } catch (error) {
                handleError(error);
            }
        },

        // Search for products based on a query string
        searchProducts: async (root, args, context, info) => {
            const { query } = args;  // Destructure query from arguments
            try {
                const response = await axios.get(`${baseURL}/products/search`, {
                    params: { query },
                });
                return response.data;
            } catch (error) {
                handleError(error);
            }
        },

        // Fetch analytics data for products
        productAnalytics: async (root, args, context, info) => {
            try {
                const response = await axios.get(`${baseURL}/products/analytics`);
                return response.data;
            } catch (error) {
                handleError(error);
            }
        },
    },

    // Resolvers for mutations
    Mutation: {
        // Add a new product
        addProduct: async (root, args, context, info) => {
            const { productInput } = args;  // Destructure productInput from arguments
            try {
                const response = await axios.post(`${baseURL}/products`, productInput);
                return response.data;
            } catch (error) {
                handleError(error);
            }
        },

        // Update an existing product by its _id
        updateProduct: async (root, args, context, info) => {
            const { _id, productInput } = args;  // Destructure _id and productInput from arguments
            try {
                const response = await axios.put(`${baseURL}/products/${_id}`, productInput);
                return response.data;
            } catch (error) {
                handleError(error);
            }
        },

        // Delete a product by its _id
        deleteProduct: async (root, args, context, info) => {
            const { _id } = args;  // Destructure _id from arguments
            try {
                const response = await axios.delete(`${baseURL}/products/${_id}`);
                return { status: "success", message: "Product successfully deleted." };
            } catch (error) {
                handleError(error);
            }
        },
    },
};

// Error handling function for axios requests
function handleError(error) {
    if (error.response) {
        if (error.response.status === 404 || error.response.status === 400) {
            throw new Error("Product not found.");
        } else {
            throw new Error("Failed to process request.");
        }
    } else if (error.request) {
        throw new Error("No response received from server.");
    } else {
        throw new Error("Error setting up the request.");
    }
}

// Export the resolvers for use in other modules
module.exports = resolvers;
