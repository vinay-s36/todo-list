from django.db import models


class User(models.Model):
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
