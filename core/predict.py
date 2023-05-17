from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import pandas as pd

# Load the data
data = pd.read_csv("business_data.csv")

# Prepare the data
X = data[["revenue", "expenses"]]
y = data["profit"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Choose a model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
print("R^2 score:", r2)

# Use the model for prediction
new_data = pd.DataFrame({"revenue": [100000], "expenses": [50000]})
prediction = model.predict(new_data)
print("Predicted profit:", prediction[0])
