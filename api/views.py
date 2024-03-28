from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *


def home(request):
    return render(request, 'api/todo.html')


@api_view(['POST'])
def add_task(request):
    try:
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def delete_task(request, id):
    try:
        task = Todo.objects.get(id=id)
        task.delete()
        return Response({"message": "Task deleted successfully"}, status=status.HTTP_200_OK)
    except KeyError:
        return Response({"message": "Task ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    except Todo.DoesNotExist:
        return Response({"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def display_tasks(request):
    try:
        tasks = Todo.objects.all()
        tasks_serializer = TaskSerializer(
            tasks, many=True, context={'request': request})
        data = {
            'tasks': tasks_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def toggle_task(request, id):
    try:
        task = Todo.objects.get(id=id)
    except Todo.DoesNotExist:
        return Response({"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
