from django.db import models
from datetime import date

# Create your models here.
class ProjectManagement(models.Model):
    name = models.CharField(max_length=100)
    priority = models.IntegerField()
    end_date = models.DateField()
    project_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    flag = models.BooleanField(default=False)

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

    def __str__(self):
        return 'id：'+ str(self.id) +'  ' + 'task_name：'+ self.name +'  '+  '  ' + 'Big_task_id：' +   str(self.task_id) + ' ' + 'project_id：' + str(self.task.project_id) + " " +"end_date：" + str(self.end_date)

    def change_str(self):
        choice = [(0, '高'),(1, '中'),(2, '低')]
        for k, y in choice:
            if k == self.priority:
                return y

    def days_left(self):
        current_date = date.today()
        return (self.end_date - current_date).days

class MiddleTask(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    priority = models.IntegerField()
    task = models.ForeignKey(ProjectTask, to_field="id", on_delete=models.CASCADE)
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    flag = models.BooleanField(default=False)

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

def get_today_task():
    #field名__dateで、日付（2019/08/01 etc ...)と一致するものが入る
    today_tasks = len(ProjectTask.objects.filter(created_at__date = date.today())) + len(MiddleTask.objects.filter(created_at__date = date.today())) + len(SmallTask.objects.filter(created_at__date = date.today()))
    today_end_tasks = len(ProjectTask.objects.filter(created_at__date = date.today(), flag=1)) + len(MiddleTask.objects.filter(created_at__date = date.today(), flag=1)) + len(SmallTask.objects.filter(created_at__date = date.today(), flag=1))
    return (today_end_tasks / today_tasks) * 100