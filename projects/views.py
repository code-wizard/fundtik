from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from applications.forms import FbApplicationForm
from applications.models import FbApplication
from fund.models import FbFunding
from projects.forms import FbProjectForm, FbMileStonesForm
from projects.models import FbProjects, FbMileStones

FbUser = get_user_model()

@login_required
def list(request):
    form = FbProjectForm()
    funding = FbFunding.objects.all()
    projects = FbProjects.objects.all()
    milestones = FbMileStones.objects.all()
    print(request.user)
    if request.method == "POST":
        data = request.POST.copy()
        data["created_by"] = request.user.uuid
        form = FbProjectForm(data, request.FILES)
        if form.is_valid():
            print(form.errors)
            data = request.POST

            form.save()

            return redirect("projects:list")
        print(form.errors)
    return render(request, "projects/list.html", context={"form": form,
                                                          "milestones": milestones,
                                                          "projects": projects,
                                                          "funding": funding})

@login_required()
def milestone(request, **kwargs):
    form = FbMileStonesForm(initial={})
    milestones = FbMileStones.objects.filter(project=kwargs.get('id'))
    project = FbProjects.objects.get(pk=kwargs.get("id"))
    users = FbUser.objects.all()
    if request.method == "POST":
        data = request.POST.copy()
        data["created_by"] = request.user.uuid
        data["project"] = project.id
        form = FbMileStonesForm(data, request.FILES)
        if form.is_valid():
            print(form.errors)

            form.save()

            form = FbProjectForm()
        print(form.errors)
    return render(request, "projects/milestones.html", {"milestones": milestones,
                                                        "form": form,
                                                        "users": users,
                                                        "project": project})


@login_required()
def tasks(request):
    return render(request, "projects/tasks.html")


@login_required()
def application(request, **kwargs):
    form = FbApplicationForm(initial={})
    project = FbProjects.objects.get(pk=kwargs.get("id"))
    applications = FbApplication.objects.filter(project=kwargs.get("id"))
    funding = project.funding.all()
    users = FbUser.objects.all()
    if request.method == "POST":
        data = request.POST.copy()
        data["created_by"] = request.user.uuid
        data["project"] = project.id
        form = FbApplicationForm(data, request.FILES)
        if form.is_valid():
            print(form.errors)

            form.save()

            form = FbApplicationForm()
        print(form.errors)
    return render(request, "applications/list.html", {"form": form,
                                                      "users": users,
                                                      "project": project,
                                                      "applications": applications, "funding": funding})