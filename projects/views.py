from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.
from applications.forms import FbApplicationForm
from applications.models import FbApplication
from fund.models import FbFunding
from projects.forms import FbProjectForm, FbMileStonesForm
from projects.models import FbProjects, FbMileStones

FbUser = get_user_model()

@login_required
def list(request):
    search_query = request.GET.get('search', '')
    projects = FbProjects.objects.all()
    
    if search_query:
        projects = projects.filter(
            Q(name__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    projects = projects.order_by('-created_at')
    form = FbProjectForm()
    funding = FbFunding.objects.all()
    milestones = FbMileStones.objects.all()
    
    context = {
        'form': form,
        'milestones': milestones,
        'projects': projects,
        'funding': funding,
        'search_query': search_query
    }
    return render(request, "projects/list.html", context)

@login_required
def project_create(request):
    if request.method == "POST":
        form = FbProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            form.save_m2m()  # Save many-to-many relationships
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True, 
                    'message': 'Project created successfully!'
                })
            return redirect("projects:list")
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False, 
                    'errors': form.errors,
                    'message': 'Please correct the errors below.'
                })
    return redirect("projects:list")

@login_required
def project_edit(request, pk):
    project = get_object_or_404(FbProjects, pk=pk)
    
    # Check if user owns the project or is admin
    if project.created_by != request.user and not request.user.is_staff:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False, 
                'message': 'You do not have permission to edit this project.'
            })
        return redirect("projects:list")
    
    if request.method == "POST":
        form = FbProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True, 
                    'message': 'Project updated successfully!'
                })
            return redirect("projects:list")
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False, 
                    'errors': form.errors,
                    'message': 'Please correct the errors below.'
                })
    return redirect("projects:list")

@login_required
def project_delete(request, pk):
    project = get_object_or_404(FbProjects, pk=pk)
    
    # Check if user owns the project or is admin
    if project.created_by != request.user and not request.user.is_staff:
        return redirect("projects:list")
    
    project.delete()
    return redirect("projects:list")

@login_required()
def milestone(request, **kwargs):
    project = get_object_or_404(FbProjects, pk=kwargs.get("id"))
    milestones = FbMileStones.objects.filter(project=project).order_by('due_date')
    users = FbUser.objects.all()
    
    if request.method == "POST":
        form = FbMileStonesForm(request.POST, request.FILES)
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.created_by = request.user
            milestone.project = project
            milestone.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True, 
                    'message': 'Milestone created successfully!'
                })
            return redirect("projects:milestone", id=project.id)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False, 
                    'errors': form.errors,
                    'message': 'Please correct the errors below.'
                })
            print("Form errors:", form.errors)
    else:
        form = FbMileStonesForm()
            
    return render(request, "projects/milestones.html", {
        "milestones": milestones,
        "form": form,
        "users": users,
        "project": project
    })


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
        form = FbApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.created_by = request.user
            application.project = project
            application.save()
            form = FbApplicationForm()  # Reset form after successful save
        else:
            print("Form errors:", form.errors)
            
    return render(request, "applications/list.html", {
        "form": form,
        "users": users,
        "project": project,
        "applications": applications, 
        "funding": funding
    })