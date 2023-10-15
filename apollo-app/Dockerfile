# Use an official Node.js runtime as a parent image
FROM node:14

# Set the working directory in the container
WORKDIR /apollo-app

# Copy package.json and package-lock.json into the container
COPY package*.json ./

# Install the Apollo Server dependencies
RUN npm install

# Copy the rest of the application code into the container
COPY . .

# The command to run the Apollo Server when the container starts
CMD ["npm", "start"]
