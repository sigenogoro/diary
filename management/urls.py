from django.urls import path
from . import views
import mydiary.views

app_name = 'management'
urlpatterns = [
    path('', views.index, name='index'),
    path('create_project/',views.create_project, name='create_project'),
    path('mydiary/', mydiary.views.index, name='change'),
    path('detail/<int:num>', views.project_detail, name ='project_detail'),
    path('create_task/<int:num>', views.create_task, name="create_task")
]