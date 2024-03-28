from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('add-task/', add_task, name='add_task'),
    path('delete-task/<int:id>/', delete_task, name='delete_task'),
    path('display-tasks/', display_tasks, name='display_tasks'),
    path('toggle-task/<int:id>/', toggle_task, name='toggle_task'),
]
