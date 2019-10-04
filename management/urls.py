from django.urls import path
from . import views
import mydiary.views

app_name = 'management'
urlpatterns = [
    path('', views.index, name='index'),
    path('mydiary/', mydiary.views.index, name='change'),
    path('up_task/<int:num>', views.update_task, name="update_task"),
    path('detail/<int:project_id>', views.big_task_detail, name ='big_task_detail'),
    path('detail/<int:project_id>/<int:big_id>', views.middle_task_detail, name ='middle_task_detail'),
    path('detail/<int:project_id>/<int:big_id>/<int:middle_id>', views.small_task_detail, name ='small_task_detail'),
    path('create_task/<int:num>', views.create_task, name="create_task"),
    path('create_project/',views.create_project, name='create_project'),
]