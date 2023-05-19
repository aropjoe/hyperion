import json
import datetime


class Subscription:
    def __init__(self, start_date, end_date, plan, amount):
        self.start_date = start_date
        self.end_date = end_date
        self.plan = plan
        self.amount = amount


def increase_and_store_data(subscriptions_data, file_path, total_items):
    expanded_data = subscriptions_data.copy()

    while len(expanded_data) < total_items:
        last_subscription = expanded_data[-1]
        new_subscription = Subscription(
            last_subscription.start_date + datetime.timedelta(days=30),
            last_subscription.end_date + datetime.timedelta(days=30),
            last_subscription.plan,
            last_subscription.amount,
        )
        expanded_data.append(new_subscription)

    data_list = []
    for subscription in expanded_data:
        data_list.append(
            {
                "start_date": subscription.start_date.strftime("%Y-%m-%d"),
                "end_date": subscription.end_date.strftime("%Y-%m-%d"),
                "plan": subscription.plan,
                "amount": subscription.amount,
            }
        )

    with open(file_path, "w") as json_file:
        json.dump(data_list, json_file, indent=4)


# Example data
subscriptions_data = [
    Subscription(datetime.date(2023, 1, 1), datetime.date(2023, 3, 31), "Basic", 100),
    Subscription(datetime.date(2023, 2, 15), datetime.date(2023, 5, 15), "Pro", 200),
    Subscription(datetime.date(2023, 3, 1), datetime.date(2023, 4, 30), "Basic", 150),
    Subscription(datetime.date(2023, 4, 1), datetime.date(2023, 4, 30), "Basic", 100),
    Subscription(datetime.date(2023, 3, 15), datetime.date(2023, 5, 31), "Pro", 250),
]

# Increase data and store in JSON
increase_and_store_data(subscriptions_data, "revenue.json", 1000)

"""
In this example, the Subscription class is defined to represent each subscription item with start and end dates, a plan name, and an amount.

The increase_and_store_data function takes three parameters: subscriptions_data, which is the initial data, file_path, which specifies the file path where the JSON file will be saved, and total_items, which represents the desired total number of items after expansion.

The function first creates a copy of the initial subscriptions_data list called expanded_data. It then uses a loop to extend the list by generating new subscriptions with incremented dates based on the last subscription in the list. The loop continues until the expanded_data list reaches the desired total_items.

Next, the function creates a list of dictionaries (data_list) where each dictionary represents a subscription item in the format specified. The datetime objects are converted to string format using strftime to ensure compatibility with JSON serialization.

Finally, the data_list is stored in a JSON file specified by file_path using the json.dump function with an indent of 4 for readability.

When you run this code, it will generate an expanded list of subscriptions with 100 items and store it in a JSON file named "expanded_data.json".

"""
