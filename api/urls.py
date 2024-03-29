from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

urlpatterns = [
    path('', loginpage, name='loginpage'),
    path('login/', user_login, name='login'),
    path('logout/', logout, name='logout'),
    path('signup/', signup, name='signup'),
    path('todo-list/', home, name='home'),
    path('api/add-task/', add_task, name='add_task'),
    path('api/delete-task/<int:id>/', delete_task, name='delete_task'),
    path('api/display-tasks/', display_tasks, name='display_tasks'),
    path('api/toggle-task/<int:id>/', toggle_task, name='toggle_task'),
]
