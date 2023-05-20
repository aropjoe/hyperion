import datetime
import json
import csv


def read_server_logs_from_json(file_path):
    with open(file_path, "r") as json_file:
        server_logs = json.load(json_file)
    return server_logs


def read_server_logs_from_csv(file_path):
    server_logs = []
    with open(file_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            server_logs.append(row)
    return server_logs


def calculate_uptime(server_logs, ext_type):
    total_uptime = datetime.timedelta(0)
    total_downtime = datetime.timedelta(0)
    uptime_start = None

    if ext_type == "json":
        for log_entry in server_logs:
            if log_entry["status"] == "up":
                if uptime_start is None:
                    uptime_start = datetime.datetime.fromisoformat(
                        log_entry["timestamp"]
                    )
            elif log_entry["status"] == "down":
                if uptime_start is not None:
                    uptime_end = datetime.datetime.fromisoformat(log_entry["timestamp"])
                    uptime_duration = uptime_end - uptime_start
                    total_uptime += uptime_duration
                    total_downtime += uptime_end - uptime_start
                    uptime_start = None

        if uptime_start is not None:
            # In case the server is still up at the end of the logs
            total_uptime += datetime.datetime.now() - uptime_start

        uptime_percentage = (total_uptime / (total_uptime + total_downtime)) * 100
        return uptime_percentage

    elif ext_type == "csv":
        for log_entry in server_logs:
            timestamp = datetime.datetime.strptime(
                log_entry["timestamp"], "%Y-%m-%d %H:%M:%S"
            )
            status = log_entry["status"]

            if status == "up":
                uptime_start = timestamp
            elif status == "down" and uptime_start is not None:
                uptime_end = timestamp
                uptime_duration = uptime_end - uptime_start
                total_uptime += uptime_duration
                total_downtime += uptime_end - uptime_start
                uptime_start = None

        uptime_percentage = (total_uptime / (total_uptime + total_downtime)) * 100
        return uptime_percentage
    else:
        return None


def calculate_average_latency(server_logs):
    latency_data = [x["latency"] for x in server_logs]
    total_latency = sum(latency_data)
    average_latency = total_latency / len(latency_data)
    return average_latency


def calculate_response_time(server_logs):
    response_times = [x["response_time"] for x in server_logs]
    max_response_time = max(response_times)
    min_response_time = min(response_times)
    average_response_time = sum(response_times) / len(response_times)
    return max_response_time, min_response_time, average_response_time

"""
file_path = "performance.json"
server_logs = read_server_logs_from_json(file_path)
uptime_percentage = calculate_uptime(server_logs, "json")
print("response_times: ", calculate_response_time(server_logs))
print("latency: ", calculate_average_latency(server_logs))
print(f"Uptime Percentage: {uptime_percentage:.2f}%")
"""
"""
In the example above, calculate_uptime function calculates the uptime percentage based on server logs that contain entries indicating whether the server was up or down at a given timestamp.

The calculate_average_latency function takes a list of latency values and calculates the average latency by summing all the values and dividing by the number of data points.

The calculate_response_time function takes a list of response times and calculates the maximum, minimum, and average response times using built-in functions max, min, and sum.

You can pass the appropriate data to these functions to calculate the desired metrics based on your specific use case.
"""
