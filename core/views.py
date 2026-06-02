from django.shortcuts import render
from .models import Project, Education, Talk


def home(request):
    projects = Project.objects.all()
    education = Education.objects.all()
    talks = Talk.objects.all()
    return render(request, 'core/index.html', {
        'projects': projects,
        'education': education,
        'talks': talks,
    })