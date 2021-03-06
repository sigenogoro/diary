from django.shortcuts import render, redirect, reverse
from .forms import PriorityForm
from .models import ProjectManagement, ProjectTask, MiddleTask, SmallTask, get_total_task, get_today_task, get_week_task
from datetime import date
from datetime import datetime
import sys
from django.utils import timezone

# Create your views here.
def index(request):
    all_project = ProjectManagement.objects.order_by('priority')[:5]
    project_form = {
        'form': PriorityForm(),
        'projects': all_project,
        'total': get_total_task(),
        'today_total': get_today_task(),
        'week_total': get_week_task(),
    }
    return render(request, 'management/index.html', project_form)

#urls.pyのname属性からメソッドを分けている
def big_task_detail(request, project_id):
    project = ProjectManagement.objects.get(project_id=project_id)
    all_big_task = project.projecttask_set.filter(flag=0).order_by("priority") #projecttask_set　リレーションしている値をとりだす
    project_form = {
        'id': project_id,
        'form': PriorityForm(),
        'big_tasks': all_big_task,
    }
    return render(request, 'management/big_task.html', project_form)

def middle_task_detail(request, project_id, big_id):
    big_task = ProjectTask.objects.get(id=big_id)
    project = ProjectManagement.objects.get(project_id=big_task.task_id)
    all_middle_task = big_task.middletask_set.filter(flag=0).order_by("priority") #projecttask_set　リレーションしている値をとりだす
    all_big_task = project.projecttask_set.filter(flag=0).order_by("priority")
    project_form = {
        'id': big_id,
        'form': PriorityForm(),
        'big_tasks': all_big_task,
        'middle_tasks': all_middle_task,
    }
    return render(request, 'management/middle_task.html', project_form)



def small_task_detail(request, project_id, big_id, middle_id):
    middle_task = MiddleTask.objects.get(id=middle_id)
    big_task = ProjectTask.objects.get(id=middle_task.task_id)
    project = ProjectManagement.objects.get(project_id=big_task.task_id)
    all_small_task = middle_task.smalltask_set.filter(flag=0).order_by("priority")
    all_middle_task = big_task.middletask_set.filter(flag=0).order_by("priority") #projecttask_set　リレーションしている値をとりだす
    all_big_task = project.projecttask_set.filter(flag=0).order_by("priority")
    project_form = {
        'id': middle_id,
        'form': PriorityForm(),
        'big_tasks': all_big_task,
        'middle_tasks': all_middle_task,
        'small_tasks': all_small_task,
    }
    return render(request, 'management/small_task.html', project_form)

def change_task(request, num):
    print(num)
    redirect_project_id = ProjectTask.objects.get(id=num).task.project_id
    if request.POST.get("decison-name") == "completion":
        redirect_project_id = task_flag(num, request.POST.get("tasktype"))
    elif request.POST.get("decison-name") == "delete":
        redirect_project_id = delete_task(num, request.POST.get("tasktype"))
    elif request.POST.get("decison-name") == "update":
        edit_big_task = ProjectTask.objects.get(id=num)
        edit_big_task.name = request.POST["name"]
        edit_big_task.priority = request.POST["priority"]
        edit_big_task.end_date = datetime.strptime(request.POST['date'], "%m/%d/%Y").strftime('%Y-%m-%d')
        edit_big_task.save()
    return redirect('management:big_task_detail', project_id=redirect_project_id)

def delete_task(task_id, task_type):
    if task_type == "middle-task":
        task = MiddleTask.objects.get(id=task_id)
        task_project_id = task.task.task.project_id
        task.delete()
    elif task_type == "small-task":
        task = SmallTask.objects.get(id=task_id)
        task_project_id = task.task.task.task.project_id
        task.delete()
    else:
        task = ProjectTask.objects.get(id=task_id)
        task_project_id = task.task.project_id
        task.delete()
    return task_project_id




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
    print(request.POST)
    if request.method == "POST":
        str_date = datetime.strptime(request.POST['date'], "%m/%d/%Y")
        change_date =  str_date.strftime('%Y-%m-%d')
        if request.POST.get("tasktype") == "big-task":
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

def task_flag(task_id, task_type):
    if task_type == "middle-task":
        task = MiddleTask.objects.get(id=task_id)
        task.flag = True
        task.update_flag_at = timezone.datetime.now()
        task.save()
        return task.task.task.project_id
    elif task_type == "small-task":
        task = SmallTask.objects.get(id=task_id)
        task.flag = True
        task.update_flag_at = timezone.datetime.now()
        task.save()
        return task.task.task.task.project_id
    else:
        task = ProjectTask.objects.get(id=task_id)
        task.flag = True
        task.update_flag_at = timezone.datetime.now()
        task.save()
        return task.task.project_id