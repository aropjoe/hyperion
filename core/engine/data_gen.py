import csv
import random
import datetime
import json


def create_csv_file(data, file_path):
    fieldnames = ["timestamp", "status", "latency", "response_time"]

    with open(file_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for entry in data:
            writer.writerow(entry)


def save_list_of_dicts_to_json(data, file_path):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


# Generate example data
data = []
start_timestamp = datetime.datetime(2023, 5, 19, 8, 0, 0)
for i in range(1020):
    timestamp = start_timestamp + datetime.timedelta(minutes=5 * i)
    status = random.choice(["up", "down"])
    latency = round(random.uniform(10, 20), 1)
    response_time = random.randint(200, 400)
    entry = {
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "status": status,
        "latency": latency,
        "response_time": response_time,
    }
    data.append(entry)

# Create the CSV file
create_csv_file(data, "performance.csv")

# Save the list of dictionaries to a JSON file
save_list_of_dicts_to_json(data, "performance.json")
