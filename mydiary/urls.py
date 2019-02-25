from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:num>', views.detail, name = 'detail'),
    path('create', views.create, name='create'),
    path('edit/<int:num>', views.edit, name='edit'),
    path('delete/<int:num>', views.delete, name='delete'),
]