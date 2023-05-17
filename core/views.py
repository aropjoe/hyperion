from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Data, Analysis
from .forms import ProjectForm, DataForm
from .utils import process_data


# from .models import Sales, Customers
def sales_vs_customers(request):
    sales_data = Sales.objects.all()
    customer_data = Customers.objects.all()

    # Merge the data sources on the common field
    merged_data = pd.merge(sales_data, customer_data, on="Customer ID")

    # Create a new column to represent total sales by customer
    merged_data["Total Sales"] = merged_data["Units Sold"] * merged_data["Unit Price"]

    # Group the data by customer name and calculate the total sales
    grouped_data = merged_data.groupby(["Customer Name"], as_index=False)[
        "Total Sales"
    ].sum()

    # Create a bar chart visualization using Plotly
    fig = px.bar(
        grouped_data, x="Customer Name", y="Total Sales", title="Sales vs. Customers"
    )

    # Convert the chart to JSON format for rendering on the template
    chart = fig.to_json()

    return render(request, "core/sales_vs_customers.html", {"chart": chart})


@login_required
def project_list(request):
    projects = Project.objects.filter(owner=request.user) | Project.objects.filter(
        collaborators=request.user
    )
    return render(request, "core/project_list.html", {"projects": projects})


@login_required
def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    if (
        request.user not in project.collaborators.all()
        and request.user != project.owner
    ):
        return redirect("project_list")
    return render(request, "core/project_detail.html", {"project": project})


@login_required
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.collaborators.add(request.user)
            return redirect("project_detail", project_id=project.id)
    else:
        form = ProjectForm()
    return render(request, "core/project_form.html", {"form": form})


@login_required
def project_edit(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.user != project.owner:
        return redirect("project_detail", project_id=project.id)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("project_detail", project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    return render(request, "core/project_form.html", {"form": form, "edit": True})


def dataset_list(request):
    datasets = Dataset.objects.all()
    return render(request, "core/datasets.html", {"datasets": datasets})


@login_required
def data_create(request, project_id):
    project = Project.objects.get(id=project_id)
    if (
        request.user != project.owner
        and request.user not in project.collaborators.all()
    ):
        return redirect("project_detail", project_id=project.id)
    if request.method == "POST":
        form = DataForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.project = project
            data.save()
            return redirect("project_detail", project_id=project.id)
    else:
        form = DataForm()
    return render(request, "core/data_form.html", {"form": form})


@login_required
def data_detail(request, data_id):
    data = Data.objects.get(id=data_id)
    if (
        request.user != data.project.owner
        and request.user not in data.project.collaborators.all()
    ):
        return redirect("project_detail", project_id=data.project.id)
    return render(request, "core/data_detail.html", {"data": data})
