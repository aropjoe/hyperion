import pandas as pd
import os
import math


def round_up_to_2_decimal(num):
    rounded_num = round(num, 2)
    rounded_up_num = math.ceil(rounded_num * 100) / 100
    return rounded_up_num


def add_commas_to_integer(num):
    formatted_num = "{:,}".format(num)
    return formatted_num


def process_data(file_path):
    # Load data from CSV file
    df = pd.read_csv(file_path)

    # Clean data
    df["date"] = pd.to_datetime(df["date"])
    df = df.dropna()

    # Calculate moving averages
    df["ma7"] = df["value"].rolling(window=7).mean()
    df["ma30"] = df["value"].rolling(window=30).mean()

    return df


def is_xls_file(file_path):
    extension = os.path.splitext(file_path)[1]
    return extension.lower() == ".xls"


def process_excel(file_path):
    if is_xls_file(file_path):
        data_frame = pd.read_excel(file_path)
        data_frame["Order Date"] = data_frame["Order Date"].dt.strftime("%Y-%m-%d")
        return data_frame
    else:
        return None


def sum_column(data_frame, column_name):
    if column_name in data_frame.columns:
        total_value = data_frame[column_name].sum()
        return total_value
    else:
        return 0


def group_sales_by_date(data_frame):
    if "Order Date" in data_frame.columns and "Sales" in data_frame.columns:
        grouped_data = data_frame.groupby("Order Date")["Sales"].sum().reset_index()
        return grouped_data
    else:
        return None


def group_profit_by_date(data_frame):
    if "Order Date" in data_frame.columns and "Profit" in data_frame.columns:
        grouped_data = data_frame.groupby("Order Date")["Profit"].sum().reset_index()
        return grouped_data
    else:
        return None


def group_sales_by_category(data_frame):
    if "Category" in data_frame.columns and "Sales" in data_frame.columns:
        grouped_data = data_frame.groupby("Category")["Sales"].sum().reset_index()
        return grouped_data
    else:
        return None


def group_sales_by_product(data_frame):
    if "Product Name" in data_frame.columns and "Sales" in data_frame.columns:
        grouped_data = data_frame.groupby("Product Name")["Sales"].sum().reset_index()
        return grouped_data
    else:
        return None


def group_sales_by_sub_category(data_frame):
    if "Sub-Category" in data_frame.columns and "Sales" in data_frame.columns:
        grouped_data = data_frame.groupby("Sub-Category")["Sales"].sum().reset_index()
        return grouped_data
    else:
        return None


def group_profit_by_category(data_frame):
    if "Category" in data_frame.columns and "Profit" in data_frame.columns:
        grouped_data = data_frame.groupby("Category")["Profit"].sum().reset_index()
        return grouped_data
    else:
        return None


def group_profit_by_sub_category(data_frame):
    if "Sub-Category" in data_frame.columns and "Profit" in data_frame.columns:
        grouped_data = data_frame.groupby("Sub-Category")["Profit"].sum().reset_index()
        return grouped_data
    else:
        return None
