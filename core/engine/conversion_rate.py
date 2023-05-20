import random


def calculate_conversion_rate(signups, purchases):
    conversion_rate = (purchases / signups) * 100
    return conversion_rate


def read_conversion_data(num_signups, conversion_rate):
    signups = num_signups
    purchases = int((conversion_rate / 100) * signups)

    # Generate random purchase events
    purchase_events = []
    for _ in range(purchases):
        event_timestamp = "2023-05-19 08:00:00"  # Replace with actual timestamp
        purchase_events.append(event_timestamp)

    return signups, purchases, purchase_events

"""
# Example usage
num_signups = 1000
conversion_rate = 5.0  # 5% conversion rate

# Generate conversion data
signups, purchases, purchase_events = generate_conversion_data(
    num_signups, conversion_rate
)

# Calculate conversion rate
conversion_rate_result = calculate_conversion_rate(signups, purchases)

print("Number of signups:", signups)
print("Number of purchases:", purchases)
print("Conversion rate:", conversion_rate_result)
print("Purchase events:", purchase_events)
"""