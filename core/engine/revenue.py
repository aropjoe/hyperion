import datetime
import json


def read_subscriptions_from_json(file_path):
    with open(file_path, "r") as json_file:
        subscriptions = json.load(json_file)
    return subscriptions


# Calculate total revenue
def total_revenue(subscriptions_data):
    return sum(subscription["amount"] for subscription in subscriptions_data)


# Calculate revenue by tier
def revenue_by_tier(subscriptions_data):
    revenue_by_tier = {}
    for subscription in subscriptions_data:
        tier = subscription["plan"]
        if tier in revenue_by_tier:
            revenue_by_tier[tier] += subscription["amount"]
        else:
            revenue_by_tier[tier] = subscription["amount"]
    return revenue_by_tier


# Calculate average revenue per subscription
def average_revenue(subscriptions_data, total_revenue):
    return total_revenue / len(subscriptions_data)


# Calculate customer lifetime value (CLTV)
def calculate_cltv(subscriptions_data):
    cltv = {}
    for subscription in subscriptions_data:
        tier = subscription["plan"]
        if tier in cltv:
            cltv[tier] += subscription["amount"]
        else:
            cltv[tier] = subscription["amount"]
    return cltv


def revenue_by_tier_array(revenue_by_tier):
    tier = []
    revenue = []

    for t, r in revenue_by_tier.items():
        tier.append(t)
        revenue.append(r)

    return tier, revenue


def cltv_array(cltv):
    tier = []
    revenue = []

    for t, r in cltv.items():
        tier.append(t)
        revenue.append(r)

    return tier, revenue
