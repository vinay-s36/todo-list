from django.db import models


class Todo(models.Model):
    title = models.CharField(max_length=120)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class User(models.Model):
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.email
