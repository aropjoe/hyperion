# Purchase Orders

def group_purchases_by_date(data_frame):
    if "PO CREATION DATE" in data_frame.columns and "PO NUMBER" in data_frame.columns:
        data_frame = data_frame.dropna()
        grouped_data = data_frame.groupby("PO CREATION DATE")["PO NUMBER"].sum().reset_index()
        data = {
            "dates": grouped_data["PO CREATION DATE"].to_list(),
            "numbers": grouped_data["PO NUMBER"].to_list(),
        }
        return data
    else:
        return None


def group_purchases_by_supplier(data_frame):
    if "SUPPLIER ACCOUNT" in data_frame.columns and "PO NUMBER" in data_frame.columns:
        data_frame = data_frame.dropna()
        grouped_data = data_frame.groupby("SUPPLIER ACCOUNT")["PO NUMBER"].sum().reset_index()
        data = {
            "suppliers": grouped_data["SUPPLIER ACCOUNT"].to_list(),
            "numbers": grouped_data["PO NUMBER"].to_list(),
        }
        return data
    else:
        return None


def group_amount_by_supplier(data_frame):
    if "SUPPLIER ACCOUNT" in data_frame.columns and "TOTAL LINE AMOUNT" in data_frame.columns:
        data_frame = data_frame.dropna()
        grouped_data = data_frame.groupby("SUPPLIER ACCOUNT")["TOTAL LINE AMOUNT"].sum().reset_index()
        data = {
            "suppliers": grouped_data["SUPPLIER ACCOUNT"].to_list(),
            "amounts": grouped_data["TOTAL LINE AMOUNT"].to_list(),
        }
        return data
    else:
        return None


def group_quantities_by_supplier(data_frame):
    if "SUPPLIER ACCOUNT" in data_frame.columns and "QTY" in data_frame.columns:
        data_frame = data_frame.dropna()
        grouped_data = data_frame.groupby("SUPPLIER ACCOUNT")["QTY"].sum().reset_index()
        data = {
            "suppliers": grouped_data["SUPPLIER ACCOUNT"].to_list(),
            "qtys": grouped_data["QTY"].to_list(),
        }
        return data
    else:
        return None


def group_purchases_by_line_number(data_frame):
    if "LineNumber" in data_frame.columns and "TOTAL LINE AMOUNT" in data_frame.columns:
        data_frame = data_frame.dropna()
        grouped_data = data_frame.groupby("LineNumber")["TOTAL LINE AMOUNT"].sum().reset_index()
        data = {
            "line_numbers": grouped_data["LineNumber"].to_list(),
            "amounts": grouped_data["TOTAL LINE AMOUNT"].to_list(),
        }
        return data
    else:
        return None


def group_purchases_by_part_number(data_frame):
    if "Part Number" in data_frame.columns and "TOTAL LINE AMOUNT" in data_frame.columns:
        data_frame = data_frame.dropna()
        grouped_data = data_frame.groupby("Part Number")["TOTAL LINE AMOUNT"].sum().reset_index()
        data = {
            "part_numbers": grouped_data["Part Number"].to_list(),
            "amounts": grouped_data["TOTAL LINE AMOUNT"].to_list(),
        }
        print(grouped_data)
        return data
    else:
        return None