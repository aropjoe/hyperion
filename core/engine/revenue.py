import datetime
import json


def read_subscriptions_from_json(file_path):
    with open(file_path, "r") as json_file:
        subscriptions = json.load(json_file)
    return subscriptions


file_path = "revenue.json"
subscriptions_data = read_subscriptions_from_json(file_path)

# Calculate total revenue
total_revenue = sum(subscription["amount"] for subscription in subscriptions_data)

# Calculate revenue by tier
revenue_by_tier = {}
for subscription in subscriptions_data:
    tier = subscription["plan"]
    if tier in revenue_by_tier:
        revenue_by_tier[tier] += subscription["amount"]
    else:
        revenue_by_tier[tier] = subscription["amount"]

# Calculate average revenue per subscription
average_revenue_per_subscription = total_revenue / len(subscriptions_data)

# Calculate customer lifetime value (CLTV)
cltv = {}
for subscription in subscriptions_data:
    tier = subscription["plan"]
    if tier in cltv:
        cltv[tier] += subscription["amount"]
    else:
        cltv[tier] = subscription["amount"]

# Print the results
print(f"Total Revenue: ${total_revenue}")
print("Revenue by Tier:")
for tier, revenue in revenue_by_tier.items():
    print(f"{tier}: ${revenue}")
print(f"Average Revenue per Subscription: ${average_revenue_per_subscription:.2f}")
print("Customer Lifetime Value (CLTV):")
for tier, revenue in cltv.items():
    print(f"{tier}: ${revenue}")
