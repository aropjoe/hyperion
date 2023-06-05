from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from core.models import Data, Project, File
from core.utils import (
    process_excel,
    group_profit_by_category,
    group_profit_by_sub_category,
    group_sales_by_category,
    group_sales_by_sub_category,
    sum_column,
    round_up_to_2_decimal,
    add_commas_to_integer,
    group_sales_by_date,
    group_profit_by_date,
    group_sales_by_product,
    # text utils
    generate_bigram_wordcloud_images,
    generate_wordcloud_images,
    generate_network_image,
    generate_chord_graph_image,
    read_text_data,
)
from core.engine.revenue import (
    calculate_cltv,
    average_revenue,
    revenue_by_tier,
    total_revenue,
    read_subscriptions_from_json,
    revenue_by_tier_array,
    cltv_array,
)
from core.engine.po import (
    group_purchases_by_date,
    group_purchases_by_supplier,
    group_amount_by_supplier,
    group_quantities_by_supplier,
    group_purchases_by_line_number,
    group_purchases_by_part_number,
)
from core.engine.conversion_rate import calculate_conversion_rate, read_conversion_data
from core.engine.performance import (
    calculate_response_time,
    calculate_average_latency,
    calculate_uptime,
    read_server_logs_from_csv,
    read_server_logs_from_json,
)
from core.sentiment import analyze_sentiment
import json
import pandas as pd


@login_required
def data_list(request):
    data = Data.objects.filter(owner=request.user)
    return render(request, "core/data_list.html", {"data": data})


@login_required
def data_detail(request, data_id):
    data = get_object_or_404(Data, pk=data_id)
    return render(request, "core/data_detail.html", {"data": data})


@login_required
def text_analysis(request, data_id):
    data = get_object_or_404(Data, pk=data_id)
    file_path = data.files.first().file.path

    try:
        reviews = read_text_data(file_path)
        error_message = ""
    except Exception as e:
        error_message = f"Error with file: {e}"
        reviews = []

    texts = []
    reviews_negative = []
    reviews_positive = []

    for review in reviews:
        a = analyze_sentiment(review.strip())
        obj = {"text": review.strip()}

        highest_value = max(a.values())
        matching_keys = [key for key, value in a.items() if value == highest_value][0]
        print(matching_keys)
        # highest_key = matching_keys[0]
        # highest_key = max(obj, key=lambda k: obj[k])

        if "pos" == matching_keys:
            reviews_positive.append(review.strip())
        elif "neu" == matching_keys:
            reviews_positive.append(review.strip())
        else:
            reviews_negative.append(review.strip())

        obj.update(a)
        texts.append(obj)

    reviews_negative = " ".join(reviews_negative)
    reviews_positive = " ".join(reviews_positive)

    bigram_image = generate_bigram_wordcloud_images(reviews_negative, reviews_positive)
    wordcloud_image = generate_wordcloud_images(reviews_positive, reviews_negative)
    network_image = generate_network_image()
    # chord_image = generate_chord_graph_image()

    context = {
        "bigram_image": bigram_image,
        "wordcloud_image": wordcloud_image,
        "network_image": network_image,
        # "chord_image": chord_image,
        "data": data,
        "texts": texts,
        "error_message": error_message,
    }
    return render(request, "core/text_analysis.html", context)


@login_required
def conversion_analytics(request, data_id):
    data = get_object_or_404(Data, pk=data_id)
    file_path = data.files.first().file.path

    # read conversion data here
    # Example usage
    num_signups = 1000
    conversion_rate = 5.0  # 5% conversion rate

    signups, purchases, purchase_events = read_conversion_data(
        num_signups, conversion_rate
    )
    conversion_rate_result = calculate_conversion_rate(signups, purchases)

    context = {
        "total_signups": signups,
        "total_purchases": purchases,
        "purchase_events": purchase_events,
        "conversion_rate_result": conversion_rate_result,
        "data": data,
    }
    template = "core/conversion_analytics.html"
    return render(request, template, context)


@login_required
def performance_metrics(request, data_id):
    data = get_object_or_404(Data, pk=data_id)
    file_path = data.files.first().file.path

    server_logs = read_server_logs_from_json(file_path)
    uptime_percentage = calculate_uptime(server_logs, "json")

    response_times_percentage = calculate_response_time(server_logs)
    average_latency = calculate_average_latency(server_logs)
    uptime_percentage = f"{uptime_percentage:.2f}%"

    stamps = [
        datetime.datetime.strptime(log_entry["timestamp"], "%Y-%m-%d %H:%M:%S")
        for log_entry in server_logs
    ]
    latency_data = [x["latency"] for x in server_logs]
    response_times = [x["response_time"] for x in server_logs]

    context = {
        "uptime_percentage": uptime_percentage,
        "stamps": stamps,
        "latency_data": latency_data,
        "response_times": response_times,
        "average_latency": average_latency,
        "response_times_percentage": response_times_percentage,
        "data": data,
    }
    template = "core/performance_metrics.html"
    return render(request, template, context)


@login_required
def subscription_analytics(request, data_id):
    data = get_object_or_404(Data, pk=data_id)
    file_path = data.files.first().file.path

    subscriptions_data = read_subscriptions_from_json(file_path)
    total_revenue = sum(subscription["amount"] for subscription in subscriptions_data)

    cltv = calculate_cltv(subscriptions_data)
    total_revenue = total_revenue(subscriptions_data)
    average_revenue = average_revenue(subscriptions_data, total_revenue)
    revenue_by_tier = revenue_by_tier(subscriptions_data)

    r_tiers, r_revenue = revenue_by_tier_array(revenue_by_tier)
    c_tiers, c_revenue = cltv_array(cltv)

    context = {
        "cltv": cltv,
        "total_revenue": total_revenue,
        "average_revenue": average_revenue,
        "revenue_by_tier": revenue_by_tier,
        "r_tiers": r_tiers,
        "r_revenue": r_revenue,
        "c_revenue": c_revenue,
        "c_tiers": c_tiers,
        "data": data,
    }
    template = "core/subscription_analytics.html"
    return render(request, template, context)


@login_required
def po_analysis(request, data_id):
    data = get_object_or_404(Data, pk=data_id)
    file_path = data.files.first().file.path
    data_frame = pd.read_csv(file_path)
    #data_frame = data_frame.dropna()
    #data_frame = process_excel(file_path)

    context = {
        "data": data,
    }
    print(data_frame)

    if data_frame is not None:
        if not data_frame.empty:
            po_creation_dates = data_frame["PO CREATION DATE"].to_list()
            po_numbers = data_frame["PO NUMBER"].to_list()
            qtys = data_frame["QTY"].to_list() 
            total_line_amounts = data_frame["TOTAL LINE AMOUNT"].to_list()
            currencies = data_frame["Currency"].to_list() 
            unit_costs = data_frame["UNIT COST "].to_list() 
            suppliers_accounts = data_frame["SUPPLIER ACCOUNT"].to_list() 
            line_numbers = data_frame["LineNumber"].to_list() 
            part_numbers = data_frame["Part Number"].to_list() 

            total_amount = sum_column(data_frame, "TOTAL LINE AMOUNT")
            total_amount = round_up_to_2_decimal(total_amount)
            total_amount = add_commas_to_integer(total_amount) # total sales

            total_qty = sum_column(data_frame, "QTY")
            print(total_qty, total_amount)
            context.update(
                {
                    "total_qty": total_qty,
                    "total_amount": total_amount,
                    "po_creation_dates": po_creation_dates,
                    "po_numbers": po_numbers,
                    "qtys": qtys,
                    "total_line_amounts": total_line_amounts,
                    "currencies": currencies,
                    "unit_costs": unit_costs,
                    "suppliers_accounts": suppliers_accounts,
                    "line_numbers": line_numbers,
                    "part_numbers": part_numbers,
                    "gpp": group_purchases_by_part_number(data_frame),
                    "gpl": group_purchases_by_line_number(data_frame),
                    "gqs": group_quantities_by_supplier(data_frame),
                    "gas": group_amount_by_supplier(data_frame),
                    "gps": group_purchases_by_supplier(data_frame),
                    "gpd": group_purchases_by_date(data_frame),
                }
            )
        else:
            context["empty_file"] = True

    return render(request, "core/order_analysis.html", context)


@login_required
def data_analysis(request, data_id):
    data = get_object_or_404(Data, pk=data_id)
    file_path = data.files.first().file.path
    data_frame = process_excel(file_path)

    context = {
        "data": data,
    }

    if data_frame is not None:
        if not data_frame.empty:
            profit = data_frame["Profit"].to_list()
            sales = data_frame["Sales"].to_list()
            city = data_frame["City"].to_list()
            category = data_frame["Category"].to_list()
            sub_category = data_frame["Sub-Category"].to_list()
            order_dates = data_frame["Order Date"].to_list()
            customer_names = data_frame["Customer Name"].to_list()

            total_sales = sum_column(data_frame, "Sales")
            total_sales = round_up_to_2_decimal(total_sales)
            total_sales = add_commas_to_integer(total_sales)

            total_profit = sum_column(data_frame, "Profit")
            total_profit = round_up_to_2_decimal(total_profit)
            total_profit = add_commas_to_integer(total_profit)

            grouped_sales_data_1 = group_sales_by_category(data_frame)
            grouped_sales_data_2 = group_sales_by_sub_category(data_frame)
            grouped_sales_data_3 = group_sales_by_date(data_frame)
            grouped_profit_data_1 = group_profit_by_category(data_frame)
            grouped_profit_data_2 = group_profit_by_sub_category(data_frame)
            grouped_profit_data_3 = group_profit_by_date(data_frame)
            grouped_sales_product_1 = group_sales_by_product(data_frame)

            gs1 = {
                "sales": grouped_sales_data_1["Sales"].to_list(),
                "categories": grouped_sales_data_1["Category"].to_list(),
            }
            gs2 = {
                "sales": grouped_sales_data_2["Sales"].to_list(),
                "sub_categories": grouped_sales_data_2["Sub-Category"].to_list(),
            }
            gs3 = {
                "sales": grouped_sales_data_3["Sales"].to_list(),
                "dates": grouped_sales_data_3["Order Date"].to_list(),
            }

            gp3 = {
                "profit": grouped_profit_data_3["Profit"].to_list(),
                "dates": grouped_profit_data_3["Order Date"].to_list(),
            }

            g_prod = {
                "sales": grouped_sales_product_1["Sales"].to_list()[:10],
                "products": grouped_sales_product_1["Product Name"].to_list()[:10],
            }

            if "order_dates" in request.GET.keys():
                selected_dates = request.GET.getlist("order_dates")

                # Filter gs3 dictionary based on selected options
                gs3["sales"] = [
                    sale
                    for sale, date in zip(gs3["sales"], gs3["dates"])
                    if date in selected_dates
                ]
                gs3["dates"] = [date for date in gs3["dates"] if date in selected_dates]

                # Filter gp3 dictionary based on selected options
                gp3["profit"] = [
                    profit
                    for profit, date in zip(gp3["profit"], gp3["dates"])
                    if date in selected_dates
                ]
                gp3["dates"] = [date for date in gp3["dates"] if date in selected_dates]

            context.update(
                {
                    "order_dates": order_dates,
                    "total_sales": total_sales,
                    "total_profit": total_profit,
                    "category": category,
                    "sub_category": sub_category,
                    "city": city,
                    "customer_names": customer_names,
                    "sales": sales,
                    "profit": profit,
                    "gs1": gs1,
                    "gs2": gs2,
                    "gs3": gs3,
                    "gp3": gp3,
                    "g_prod": g_prod,
                    "grouped_sales_data_2": grouped_sales_data_2,
                    "grouped_profit_data_1": grouped_profit_data_1,
                    "grouped_profit_data_2": grouped_profit_data_2,
                    "data": data,
                }
            )
        else:
            context["empty_file"] = True

    return render(request, "core/data_analysis.html", context)


@login_required
def data_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")

        project_id = request.POST.get("project_id")
        project = get_object_or_404(Project, pk=project_id)

        data = Data(
            name=name, description=description, project=project, owner=request.user
        )
        data.save()

        files = request.FILES.getlist("files")
        for file in files:
            file_obj = File.objects.create(file=file)
            data.files.add(file_obj)

        return redirect("core:data_detail", data_id=data.id)

    projects = Project.objects.filter(owner=request.user)
    return render(request, "core/data_create.html", {"projects": projects})


@login_required
def data_upload(request, data_id):
    if request.method == "POST":
        data = get_object_or_404(Data, pk=data_id)

        files = request.FILES.getlist("files")
        for file in files:
            file_obj = File.objects.create(file=file)
            data.files.add(file_obj)

        return redirect("core:data_detail", data_id=data_id)
    else:
        return redirect("core:data_detail", data_id=data_id)


@login_required
def data_update(request, data_id):
    data = get_object_or_404(Data, pk=data_id)

    if request.method == "POST":
        data.name = request.POST.get("name")
        data.description = request.POST.get("description")
        project_id = request.POST.get("project_id")
        project = get_object_or_404(Project, pk=project_id)
        data.project = project
        data.save()

        return redirect("core:data_detail", data_id=data.id)

    projects = Project.objects.filter(owner=request.user)
    return render(
        request, "core/data_update.html", {"data": data, "projects": projects}
    )


@login_required
def data_delete(request, data_id):
    data = get_object_or_404(Data, pk=data_id)

    if request.method == "POST":
        data.delete()
        return redirect("core:data_list")

    return render(request, "core/data_delete.html", {"data": data})
