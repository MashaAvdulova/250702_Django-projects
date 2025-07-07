from django.shortcuts import render
from .models import Projects, Tag
from .forms import ProjectForm

# from fourth.devsearch.projects.models import Projects


# Create your views here.
def projects(request):
    pr = Projects.objects.all()
    context = {
        'projects' : pr,
    }
    return render(request, "projects/projects.html", context)

def project(request, pk):
    project_obj = Projects.objects.get(id=pk)

    return render(request, 'projects/single-project.html', {'project': project_obj})

def create_project(request):
    form = ProjectForm()
    context = {
        'form': form,
    }
    return render(request, "projects/form-template.html", context)