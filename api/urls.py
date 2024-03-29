from django.urls import path
from .views import *

urlpatterns = [
    path('', loginpage, name='loginpage'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('todo-list/', home, name='home'),
    path('api/add-task/', add_task, name='add_task'),
    path('api/delete-task/<int:id>/', delete_task, name='delete_task'),
    path('api/display-tasks/', display_tasks, name='display_tasks'),
    path('api/toggle-task/<int:id>/', toggle_task, name='toggle_task'),
]
