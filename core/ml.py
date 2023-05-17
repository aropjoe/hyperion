# views.py

from django.shortcuts import render
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from statsmodels.tsa.arima.model import ARIMA
from .models import Sales, Customers


def clustering(request):
    customer_data = Customers.objects.all()

    # Prepare the data for clustering
    X = np.array(customer_data[["Age", "Income"]])
    kmeans = KMeans(n_clusters=3).fit(X)
    customer_data["Cluster"] = kmeans.labels_

    # Render the results on the template
    return render(request, "clustering.html", {"customer_data": customer_data})


def linear_regression(request):
    sales_data = Sales.objects.all()

    # Prepare the data for linear regression
    X = np.array(sales_data["Units Sold"]).reshape((-1, 1))
    y = np.array(sales_data["Total Revenue"])
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0
    )
    model = LinearRegression().fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)

    # Render the results on the template
    return render(request, "linear_regression.html", {"r2": r2})


def forecasting(request):
    sales_data = Sales.objects.all()

    # Prepare the data for forecasting
    sales_data["Order Date"] = pd.to_datetime(sales_data["Order Date"])
    sales_data.set_index("Order Date", inplace=True)
    model = ARIMA(sales_data["Total Revenue"], order=(1, 1, 1))
    results = model.fit()

    # Forecast future sales
    future_dates = pd.date_range(start="2023-05-12", end="2024-05-12")
    future_data = pd.DataFrame(index=future_dates, columns=["Total Revenue"])
    future_data["Total Revenue"] = results.predict(
        start=len(sales_data), end=len(sales_data) + 11, dynamic=False
    )

    # Render the results on the template
    return render(request, "forecasting.html", {"future_data": future_data})
