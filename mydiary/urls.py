from django.urls import path, include
from . import views
import management.views

app_name = 'mydiary'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:num>', views.detail, name = 'detail'),
    path('create', views.create, name='create'),
    path('edit/<int:num>', views.edit, name='edit'),
    path('delete/<int:num>', views.delete, name='delete'),
    path('management/', management.views.index, name = 'change')
]