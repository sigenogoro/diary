from django.urls import path
from . import views
import mydiary.views

app_name = 'management'
urlpatterns = [
    path('', views.index, name='index'),
    path('mydiary/', mydiary.views.index, name='change'),
    path('detail/', views.project_detail, name ='project_detail')
]