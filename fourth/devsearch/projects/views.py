from django.shortcuts import render
from .models import Projects

# from fourth.devsearch.projects.models import Projects


# Create your views here.
def projects(request):
    pr = Projects.objects.all()
    context = {
        'projects' : pr,
    }
    return render(request, "projects/projects.html", context)