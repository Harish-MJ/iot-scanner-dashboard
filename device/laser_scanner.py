import time
import random
import json
import os
from datetime import datetime
import requests

# file path for logging data
log_file_path = "data/laser_scanner_data.log"
#cloud_server = "http://localhost:5000/data"  
cloud_server = "https://iot-scanner-dashboard.onrender.com/api/data"
# cloud_server = "http://host.docker.internal:5000/data"  # for running inside Docker?
time_interval = 10  # Time interval in seconds

# Ensure directory exists
if not os.path.exists("data"):
    os.makedirs("data")

# Function to generate 2D laser scanner data (angle, distance, intensity)
def generate_laser_scanner_data():
    num_measurements = 36  # One measurement every 10 degrees
    distance_measurements = []
    for i in range(num_measurements):
        angle = i * 10
        distance = random.uniform(100.0, 1000.0)  # Simulate distance in mm
        intensity = random.uniform(0.0, 1.0)  # Simulate intensity
        distance_measurements.append({
            "angle": angle,
            "distance": distance,
            "intensity": intensity
        })
    timestamp = datetime.utcnow().isoformat()
    return {
        "timestamp": timestamp,
        "measurements": distance_measurements
    }

# Function to write data to a local file
def log_data(data, file_path):
    with open(file_path, "a") as log_file:
        log_file.write(json.dumps(data) + "\n")

# Function to read logdata from local file
def read_logged_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as log_file:
            return log_file.readlines()
    return []

# Function to clear log data file after data transfer
def clear_log_file(file_path):
    open(file_path, 'w').close()

# Function to transfer data to the cloud
def transfer_data_to_cloud(data, endpoint):
    try:
        response = requests.post(endpoint, json=data)
        if response.status_code == 200:
            return True
        else:
            print(f"Failed to transfer data: {response.status_code}, {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error during data transfer: {e}")
        return False

# Function to check internet connectivity by pinging to google.com
def check_internet_connectivity():
    try:
        response = requests.get("http://www.google.com", timeout=5)
        return response.status_code == 200
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return False

# Function to handle data storage and transfer
def handle_data_storage_and_transfer(data):
    if check_internet_connectivity():
        # locally logged data first
        logged_data = read_logged_data(log_file_path)
        if logged_data:
            all_data = [json.loads(entry) for entry in logged_data]
            all_data.append(data)  # Include current data
            if transfer_data_to_cloud(all_data, cloud_server):
                clear_log_file(log_file_path)
                print("Logged data and current data uploaded. Local log cleared.")
            else:
                print("Failed to upload logged data. Logging current data locally.")
                log_data(data, log_file_path)
        else:
            if transfer_data_to_cloud(data, cloud_server):
                print("Current data uploaded successfully.")
            else:
                print("Failed to upload current data. Logging locally.")
                log_data(data, log_file_path)
    else:
        # No internet connectivity, log data locally
        log_data(data, log_file_path)
        print("No connection. Data logged locally.")

def main():
    while True:
        data = generate_laser_scanner_data()
        #print(f"Generated data: {data}")
        handle_data_storage_and_transfer(data)
        time.sleep(time_interval)

if __name__ == "__main__":
    main()
