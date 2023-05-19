from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from core.models import Project, Data


@login_required
def project_list(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, "core/project_list.html", {"projects": projects})


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    datasets = Data.objects.filter(project=project)
    return render(
        request, "core/project_detail.html", {"project": project, "datasets": datasets}
    )


@login_required
def project_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        owner = request.user

        project = Project(name=name, description=description, owner=owner)
        project.save()
        project.collaborators.add(request.user)

        return redirect("core:project_detail", project_id=project.id)

    projects = Project.objects.filter(owner=request.user)
    return render(request, "core/project_create.html", {"projects": projects})


@login_required
def project_update(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if request.method == "POST":
        project.name = request.POST.get("name")
        project.description = request.POST.get("description")
        project.save()

        return redirect("core:project_detail", project_id=project.id)

    return render(request, "core/project_update.html", {"project": project})


@login_required
def project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        project.delete()
        return redirect("core:project_list")
    return render(request, "core/project_delete.html", {"project": project})
