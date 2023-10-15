const { gql } = require("apollo-server");

const typeDefs = gql`
  type ProductAnalytics {
    most_common_category: String!
    avg_price_most_common_category: Float!
    total_products: Int!
  }

  type Product {
    _id: ID!
    product_name: String!
    product_category: String!
    price: Float!
    available_quantity: Int!
    description: String!
  }

  input ProductInput {
    product_name: String!
    product_category: String!
    price: Float!
    available_quantity: Int!
    description: String!
  }

  type Mutation {
    addProduct(productInput: ProductInput!): Product!
    updateProduct(_id: ID!, productInput: ProductInput!): Product!
    deleteProduct(_id: ID!): Boolean!
  }

  type Query {
    products: [Product!]!
    product(_id: ID!): Product
    searchProducts(query: String!): [Product!]!
    productAnalytics: ProductAnalytics!
  }
`;

module.exports = typeDefs;
