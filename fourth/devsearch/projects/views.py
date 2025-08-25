from django.shortcuts import render, redirect
from .models import Projects, Tag
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required



# from fourth.devsearch.projects.models import Projects


# Create your views here.
def projects(request):
    pr = Projects.objects.all()
    context = {
        'projects' : pr,
    }
    return render(request, "projects/projects.html", context)

@login_required(login_url='login')
def project(request, pk):
    project_obj = Projects.objects.get(id=pk)

    return render(request, 'projects/single-project.html', {'project': project_obj})

@login_required(login_url='login')
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            form.save()
            return redirect('projects')

    context = {
        'form': form,
    }
    return render(request, 'projects/form-template.html', context)


@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    project = profile.projects_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        new_tags = request.POST.get('tags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.projects_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    context = {'project': project}
    return render(request, 'projects/delete.html', context)