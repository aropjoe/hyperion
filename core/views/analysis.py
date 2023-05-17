from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from core.models import Analysis, Project, Data


@login_required
def analysis_list(request):
    analyses = Analysis.objects.filter(user=request.user)
    return render(request, "core/analysis_list.html", {"analyses": analyses})


@login_required
def analysis_detail(request, analysis_id):
    analysis = get_object_or_404(Analysis, id=analysis_id, user=request.user)
    return render(request, "core/analysis_detail.html", {"analysis": analysis})


@login_required
def analysis_create(request):
    if request.method == "POST":
        title = request.POST["title"]
        data_id = request.POST["data_id"]
        insights = request.POST["insights"]
        data = Data.objects.get(id=data_id)
        analysis = Analysis.objects.create(
            title=title, data=data, insights=insights, user=request.user
        )
        return redirect("core:analysis_detail", analysis_id=analysis.id)
    else:
        # Render the form for creating an analysis
        return render(request, "core/analysis_create.html")


@login_required
def analysis_update(request, analysis_id):
    analysis = get_object_or_404(Analysis, id=analysis_id, user=request.user)
    if request.method == "POST":
        analysis.title = request.POST["title"]
        analysis.insights = request.POST["insights"]
        analysis.save()
        return redirect("core:analysis_detail", analysis_id=analysis.id)
    else:
        # Render the form for updating the analysis
        return render(request, "core/analysis_update.html", {"analysis": analysis})


@login_required
def analysis_delete(request, analysis_id):
    analysis = get_object_or_404(Analysis, id=analysis_id, user=request.user)
    if request.method == "POST":
        analysis.delete()
        return redirect("core:analysis_list")
    else:
        # Render the confirmation page for deleting the analysis
        return render(request, "core/analysis_delete.html", {"analysis": analysis})
