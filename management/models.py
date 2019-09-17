from django.db import models
from datetime import date

# Create your models here.
class ProjectManagement(models.Model):
    project_name = models.CharField(max_length=100)
    priority = models.IntegerField()
    end_date = models.DateField()
    project_id = models.AutoField(primary_key=True)

    #shellモードなどに使える + modelから呼び出すときに、この形で返ってくる
    def __str__(self):
        return 'project_name：'+ self.project_name +'  '+ 'priority：' + str(self.priority) + '   ' + 'date：' +   str(self.end_date) + ' ' + 'project_id：' + str(self.project_id)

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
    title = models.CharField(max_length=100)
    priority = models.IntegerField()
    big_task = models.ForeignKey(ProjectManagement, to_field='project_id', on_delete=models.CASCADE)
    end_task = models.DateField()

    def __str__(self):
        return 'task_name：'+ self.title +'  '+ 'priority：' + str(self.priority) + '  ' + 'Big_task_id：' +   str(self.big_task_id) + ' ' + 'project_id：' + str(self.big_task.project_id) + " " +"end_task：" + str(self.end_task)

    def change_str(self):
        choice = [(0, '高'),(1, '中'),(2, '低')]
        for k, y in choice:
            if k == self.priority:
                return y

class MiddleTask(models.Model):
    id = models.AutoField(primary_key=True)
    middle_task_name = models.CharField(max_length=100)
    priority = models.IntegerField()
    middle_task = models.ForeignKey(ProjectTask, to_field="id" ,on_delete=models.CASCADE)
    end_task = models.DateField()