require('dotenv').config();
const { ApolloServer } = require('apollo-server');
const typeDefs = require('./schema');
const resolvers = require('./resolvers');

// Define the port to use for the GraphQL server
const apolloPort = process.env.APOLLO_PORT;

const server = new ApolloServer({ typeDefs, resolvers });

server.listen({ port: apolloPort }).then(({ url }) => {
    console.log(`🚀  Server ready at ${url}`);
});
