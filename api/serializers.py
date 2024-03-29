from .models import *
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['user', 'title']


class AllTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'


class OneTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['completed']
