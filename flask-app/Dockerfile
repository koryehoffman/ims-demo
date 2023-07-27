# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./

# --no-cache-dir is used to avoid caching the index locally, which is unnecessary in a containerized environment
RUN pip install --no-cache-dir -r requirements.txt 

# Copy the current directory contents into the container
COPY . .

# Run script when the container launches
CMD ["python", "app.py"]
