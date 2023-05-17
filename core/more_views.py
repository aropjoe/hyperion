# views.py

from django.shortcuts import render
import pandas as pd
from .models import Sales


def custom_calculations(request):
    sales_data = Sales.objects.all()

    # Perform custom calculations on the sales data
    sales_data["Profit Margin"] = (
        sales_data["Total Revenue"] - sales_data["Total Cost"]
    ) / sales_data["Total Revenue"]

    # Render the results on the template
    return render(request, "custom_calculations.html", {"sales_data": sales_data})


def parameters(request):
    sales_data = Sales.objects.all()

    # Retrieve parameters from the request
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    # Filter the sales data based on the parameters
    sales_data["Order Date"] = pd.to_datetime(sales_data["Order Date"])
    sales_data = sales_data[
        (sales_data["Order Date"] >= start_date)
        & (sales_data["Order Date"] <= end_date)
    ]

    # Render the results on the template
    return render(request, "parameters.html", {"sales_data": sales_data})


def filters(request):
    sales_data = Sales.objects.all()

    # Retrieve filters from the request
    product = request.GET.get("product")
    region = request.GET.get("region")

    # Filter the sales data based on the filters
    if product:
        sales_data = sales_data[sales_data["Product"] == product]
    if region:
        sales_data = sales_data[sales_data["Region"] == region]

    # Render the results on the template
    return render(request, "filters.html", {"sales_data": sales_data})
