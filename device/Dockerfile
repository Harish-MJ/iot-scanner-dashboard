# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /device

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory for data logging
RUN mkdir -p /device/data

# Copy the rest of the application code into the container
COPY . .

# Command to run the Python script
CMD ["python", "laser_scanner.py"]
