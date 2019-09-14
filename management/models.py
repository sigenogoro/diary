from django.db import models
from datetime import date

# Create your models here.
class ProjectManagement(models.Model):
    project_name = models.CharField(max_length=100)
    priority = models.IntegerField()
    end_date = models.DateField()

    #shellモードなどに使える + modelから呼び出すときに、この形で返ってくる
    def __str__(self):
        return 'project_name：'+ self.project_name +'  '+ 'priority：' + str(self.priority) + '   ' + 'date：' +   str(self.end_date)

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



class ProjectTask(models.Model):
    pass

