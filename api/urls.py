from django.urls import path
from .views import *

urlpatterns = [
    path('', loginpage, name='loginpage'),
    path('login/', user_login, name='login'),
    path('logout/', logout, name='logout'),
    path('signup/', signup, name='signup'),
    path('todo-list/', home, name='home'),
    path('api/task', add_task, name='add_task'),
    path('api/task/<int:id>', delete_task, name='delete_task'),
    path('api/tasks/<int:user_id>', display_tasks, name='display_tasks'),
    path('api/toggle-task/<int:id>', toggle_task, name='toggle_task'),
]
