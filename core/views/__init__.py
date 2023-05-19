from .analysis import *
from .data import *
from .project import *


def dashboard(request):
    context = {"user": request.user}
    template = "core/dashboard.html"
    return render(request, template, context)
