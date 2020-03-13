from django.db import models
from datetime import date
import calendar
import datetime


# Create your models here.
class ProjectManagement(models.Model):
    name = models.CharField(max_length=100)
    priority = models.IntegerField()
    end_date = models.DateField()
    project_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    flag = models.BooleanField(default=False)
    update_flag_at = models.DateTimeField(blank=True, null=True)

    #shellモードなどに使える + modelから呼び出すときに、この形で返ってくる
    def __str__(self):
        return 'project_name：'+ self.name +'  '+ 'priority：' + str(self.priority) + '   ' + 'date：' +   str(self.end_date) + ' ' + 'project_id：' + str(self.project_id)

    # ここで書いてあるメソッドは、テンプレートで使うことができる
    def change_str(self):
        choice = [(0, '高'),(1, '中'),(2, '低')]
        for k, y in choice:
            if k == self.priority:
                return y

    # マイナスを無くした方が見た目が良いかも
    def days_left(self):
        current_date = date.today()
        return (self.end_date - current_date).days


# 達成すべきタスク プロジェクト => 達成すべきタスク（big_type) => 細かいタスク(middle_task) => 小さいタスク(small_task)
class ProjectTask(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    priority = models.IntegerField()
    task = models.ForeignKey(ProjectManagement, to_field='project_id', on_delete=models.CASCADE)
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    flag = models.BooleanField(default=False)
    update_flag_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return 'id：'+ str(self.id) +' ' + 'task_name：'+ self.name +' ' + 'Big_task_id：' +   str(self.task_id) + ' ' + 'project_id：' + str(self.task.project_id) + " " +"end_date：" + str(self.end_date)

    def change_str(self):
        choice = [(0, '高'),(1, '中'),(2, '低')]
        for k, y in choice:
            if k == self.priority:
                return y

    def days_left(self):
        current_date = date.today()
        return (self.end_date - current_date).days

    def sample_1(self):
        change_date =  self.end_date.strftime('%m/%d/%Y')
        return change_date


class MiddleTask(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    priority = models.IntegerField()
    task = models.ForeignKey(ProjectTask, to_field="id", on_delete=models.CASCADE)
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    flag = models.BooleanField(default=False)
    update_flag_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return 'id：'+ str(self.id) +'  ' + 'task_name：'+ self.name +'  '+ '  ' + 'project_task_id：' +   str(self.task.task_id) + ' ' + 'Big_task_id：' + str(self.task_id) + " " +"end_date：" + str(self.end_date)


    def change_str(self):
        choice = [(0, '高'),(1, '中'),(2, '低')]
        for k, y in choice:
            if k == self.priority:
                return y

    def days_left(self):
        current_date = date.today()
        return (self.end_date - current_date).days

class SmallTask(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    priority = models.IntegerField()
    task = models.ForeignKey(MiddleTask, to_field="id", on_delete=models.CASCADE)
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    flag = models.BooleanField(default=False)
    update_flag_at = models.DateTimeField(blank=True, null=True)

    def change_str(self):
        choice = [(0, '高'),(1, '中'),(2, '低')]
        for k, y in choice:
            if k == self.priority:
                return y

    def days_left(self):
        current_date = date.today()
        return (self.end_date - current_date).days

    def __str__(self):
        return 'id：' +  str(self.id) + " " + 'task_name：'+ self.name + " " + 'middle_task_id：' +   str(self.task_id) + ' ' + 'Big_task_id：' + str(self.task.task_id) + " " +  "project_id："  +   str(self.task.task.task.project_id) + "   " +"end_date：" + str(self.end_date)



def get_total_task():
    total_number_tasks = len(ProjectTask.objects.all()) + len(MiddleTask.objects.all()) + len(SmallTask.objects.all())
    total_end_tasks = len(ProjectTask.objects.filter(flag=1)) + len(MiddleTask.objects.filter(flag=1)) + len(SmallTask.objects.filter(flag=1))
    if total_end_tasks == 0 and total_number_tasks == 0:
        return 100
    return (total_end_tasks / total_number_tasks) * 100

#update_flag_taskと同じ日 and flag=1の値を取ってくる
def get_today_task():
    #field名__dateで、日付（2019/08/01 etc ...)と一致するものが入る
    today_end_tasks = len(ProjectTask.objects.filter(update_flag_at__date = date.today(), flag=1)) + len(MiddleTask.objects.filter(update_flag_at__date = date.today(), flag=1)) + len(SmallTask.objects.filter(update_flag_at__date = date.today(), flag=1))
    if today_end_tasks == 0:
        return 0
    return today_end_tasks

def get_week_task():
    dt = calendar.Calendar()
    today_date = date.today()
    for week_list in dt.monthdatescalendar(today_date.year, today_date.month):
        for day in week_list:
            if day == date.today():
                week_satrt, week_end = week_list[0], week_list[0] + datetime.timedelta(days=8)
    today_end_tasks = len(ProjectTask.objects.filter(update_flag_at__range =(week_satrt, week_end))) + len(MiddleTask.objects.filter(update_flag_at__range =(week_satrt, week_end))) + len(SmallTask.objects.filter(update_flag_at__range =(week_satrt, week_end)))
    if today_end_tasks == 0:
        return 0
    return today_end_tasks

