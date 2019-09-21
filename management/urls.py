from django.urls import path
from . import views
import mydiary.views

app_name = 'management'
urlpatterns = [
    path('', views.index, name='index'),
    path('mydiary/', mydiary.views.index, name='change'),
    path('up_task/<int:num>', views.update_task, name="update_task"),
    path('detail/<int:num>', views.big_task_detail, name ='big_task_detail'),
    path('detail/2/<int:num>', views.middle_task_detail, name ='middle_task_detail'),
    path('detail/2/43/<int:num>', views.small_task_detail, name ='small_task_detail'),
    path('create_task/<int:num>', views.create_task, name="create_task"),
    path('create_project/',views.create_project, name='create_project'),
]