from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .forms import PriorityForm
from .models import ProjectManagement, ProjectTask, MiddleTask
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
def project_detail(request, num):
    project = ProjectManagement.objects.get(project_id=num)
    all_project = project.projecttask_set.all() #projecttask_set　リレーションしている値をとりだす
    current_time = date.today()
    project_form = {
        'id': num,
        'form': PriorityForm(),
        'projects': all_project,
    }
    return render(request, 'management/detail.html', project_form)

# プロジェクト作り
def create_project(request):
    if request.method == "POST":
        str_date = datetime.strptime(request.POST['date'], "%m/%d/%Y")
        change_date = str_date.strftime('%Y-%m-%d')
        ProjectManagement.objects.create(
            project_name = request.POST['task'],
            priority = request.POST['priority'],
            end_date = change_date,
        )
        return redirect(to='/management')

# タスク作り
def create_task(request, num):
    if request.method == "POST":
        str_date = datetime.strptime(request.POST['date'], "%m/%d/%Y")
        change_date = str_date.strftime('%Y-%m-%d')
        if request.POST.get("tasktype", "") == "big_task":
            ProjectTask.objects.create(
                title = request.POST['task'],
                priority = request.POST['priority'],
                end_task = change_date,
                big_task = ProjectManagement.objects.get(project_id=num)
            )
            return redirect('management:project_detail', num=num)
        elif request.POST.get("tasktype", "") == "middle-task":
            MiddleTask.objects.create(
                middle_task_name = request.POST['task'],
                priority = request.POST['priority'],
                end_task = change_date,
                middle_task = ProjectTask.objects.get(id=num)
            )
            return redirect('management:project_detail', num=num)
