from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PriorityForm
from .models import ProjectManagement
from datetime import date
from datetime import datetime

# Create your views here.
def index(request):
    all_project = ProjectManagement.objects.all()
    current_time = date.today()
    project_form = {
        'form': PriorityForm(),
        'projects': all_project,
    }
    return render(request, 'management/index.html', project_form)

#urls.pyのname属性からメソッドを分けている
def project_detail(request):
    return render(request, 'management/detail.html')


def create_project(request):
    if request.method == "POST":
        str_date = datetime.strptime(request.POST['date'], "%m/%d/%Y")
        change_date = str_date.strftime('%Y-%m-%d')
        ProjectManagement.objects.create(
            project_name = request.POST['project_name'],
            priority = request.POST['priority'],
            end_date = change_date
        )
        return redirect(to='/management')