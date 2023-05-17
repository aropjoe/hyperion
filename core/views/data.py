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
)
import json


def data_list(request):
    data = Data.objects.all()
    return render(request, "core/data_list.html", {"data": data})


def data_detail(request, data_id):
    data = get_object_or_404(Data, pk=data_id)
    return render(request, "core/data_detail.html", {"data": data})


def text_analysis(request, data_id):
    data = get_object_or_404(Data, pk=data_id)
    # file_path = data.files.first().file.path

    bigram_image = generate_bigram_wordcloud_images()
    wordcloud_image = generate_wordcloud_images()
    #network_image = generate_network_image()
    #chord_image = generate_chord_graph_image()

    context = {
        "bigram_image": bigram_image,
        "wordcloud_image": wordcloud_image,
        #"network_image": network_image,
        #"chord_image": chord_image,
        "data": data,
    }
    return render(request, "core/text_analysis.html", context)


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

    projects = Project.objects.all()
    return render(request, "core/data_create.html", {"projects": projects})


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

    projects = Project.objects.all()
    return render(
        request, "core/data_update.html", {"data": data, "projects": projects}
    )


def data_delete(request, data_id):
    data = get_object_or_404(Data, pk=data_id)

    if request.method == "POST":
        data.delete()
        return redirect("core:data_list")

    return render(request, "core/data_delete.html", {"data": data})
