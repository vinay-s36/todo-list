from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from apscheduler.triggers.cron import CronTrigger
from .models import Todo
from todo.settings import EMAIL_HOST_USER


def send_pending_tasks_email():
    pending_tasks = Todo.objects.filter(
        completed=False).select_related('user').all()

    user_task_mapping = {}
    for task in pending_tasks:
        user_task_mapping.setdefault(task.user.email, []).append(task.title)

    for email, tasks in user_task_mapping.items():
        task_list = "\n".join(tasks)
        send_mail(
            subject='Pending Tasks Notification',
            message=f'Hello,\n\nYou have the following pending tasks:\n\n{task_list}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
        )


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_pending_tasks_email,
                      CronTrigger(hour=18, minute=0))
    scheduler.start()
