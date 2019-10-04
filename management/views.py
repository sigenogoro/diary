from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .forms import PriorityForm
from .models import ProjectManagement, ProjectTask, MiddleTask, SmallTask
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

def update_task(request, num):
    if request.method == "POST":
        if request.POST.getlist('checks'):
            # リスト型だが、文字列の数値のため、数値に変えました
            list_checks = [int(i) for i in request.POST.getlist('checks')]
            for i in list_checks:
                middle_task = MiddleTask.objects.get(id=i)
                middle_task.middle_task_flag = 1
                middle_task.save()
            return redirect('management:middle_task_detail', num=num)
        return redirect(to='/management')

#urls.pyのname属性からメソッドを分けている
def big_task_detail(request, project_id):
    project = ProjectManagement.objects.get(project_id=project_id)
    all_project = project.projecttask_set.all() #projecttask_set　リレーションしている値をとりだす
    current_time = date.today()
    project_form = {
        'id': project_id,
        'form': PriorityForm(),
        'big_tasks': all_project,
    }
    return render(request, 'management/big_task.html', project_form)

def middle_task_detail(request, project_id, big_id):
    big_task = ProjectTask.objects.get(id=big_id)
    project = ProjectManagement.objects.get(project_id=big_task.task_id)
    all_middle_task = big_task.middletask_set.all() #projecttask_set　リレーションしている値をとりだす
    all_project = project.projecttask_set.all()
    current_time = date.today()
    project_form = {
        'id': big_id,
        'form': PriorityForm(),
        'big_tasks': all_project,
        'middle_tasks': all_middle_task
    }
    return render(request, 'management/middle_task.html', project_form)

def small_task_detail(request, project_id, big_id, middle_id):
    middle_task = MiddleTask.objects.get(id=middle_id)
    big_task = ProjectTask.objects.get(id=middle_task.task_id)
    project = ProjectManagement.objects.get(project_id=big_task.task_id)
    all_small_task = middle_task.smalltask_set.all()
    all_middle_task = big_task.middletask_set.all() #projecttask_set　リレーションしている値をとりだす
    all_project = project.projecttask_set.all()
    current_time = date.today()
    project_form = {
        'id': middle_id,
        'form': PriorityForm(),
        'big_tasks': all_project,
        'middle_tasks': all_middle_task,
        'small_tasks': all_small_task
    }
    return render(request, 'management/small_task.html', project_form)

# プロジェクト作り
def create_project(request):
    if request.method == "POST":
        str_date = datetime.strptime(request.POST['date'], "%m/%d/%Y")
        change_date = str_date.strftime('%Y-%m-%d')
        ProjectManagement.objects.create(
            name = request.POST['name'],
            priority = request.POST['priority'],
            end_date = change_date,
        )
        return redirect(to='/management')

# タスク作り
def create_task(request, num):
    if request.method == "POST":
        str_date = datetime.strptime(request.POST['date'], "%m/%d/%Y")
        change_date =  str_date.strftime('%Y-%m-%d')
        if request.POST.get("tasktype", "") == "big-task":
            try:
                ProjectManagement.objects.get(project_id=num)
            except ProjectManagement.DoesNotExist:
                num = ProjectTask.objects.get(id=num).task_id
                ProjectTask.objects.create(
                    name = request.POST['name'],
                    priority = request.POST['priority'],
                    end_date = change_date,
                    task = ProjectManagement.objects.get(project_id=num)
                )
                return redirect('management:big_task_detail', project_id=num)
            ProjectTask.objects.create(
                name = request.POST['name'],
                priority = request.POST['priority'],
                end_date = change_date,
                task = ProjectManagement.objects.get(project_id=num)
            )
            return redirect('management:big_task_detail', project_id=num)
        elif request.POST.get("tasktype", "") == "middle-task":
            big_task = ProjectTask.objects.get(id=num)
            MiddleTask.objects.create(
                name = request.POST['name'],
                priority = request.POST['priority'],
                end_date = change_date,
                task = ProjectTask.objects.get(id=num)
            )
            return redirect('management:middle_task_detail', project_id=big_task.task_id ,big_id=num)
        elif request.POST.get("tasktype", "") == "small-task":
            get_middle_task = MiddleTask.objects.get(id=num)
            big_task_id = get_middle_task.task_id
            project_id = get_middle_task.task.task_id
            SmallTask.objects.create(
                name = request.POST['name'],
                priority = request.POST['priority'],
                end_date = change_date,
                task = get_middle_task
            )
            return redirect('management:small_task_detail', project_id=project_id, big_id=big_task_id, middle_id=get_middle_task.id)