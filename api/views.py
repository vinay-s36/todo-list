from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *


def home(request):
    user_id = request.GET.get('user')
    user = User.objects.get(id=user_id) if user_id else None
    user_email = (user.email).split('@')[0]
    return render(request, 'api/todo.html', {'user': user, 'user_email': user_email})


def loginpage(request):
    return render(request, 'api/login.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['login-email']
        password = request.POST['login-password']
        try:
            user = User.objects.get(email=email, password=password)
            if user:
                redirect_url = f'/todo-list?user={user.id}'
                return redirect(redirect_url)
            else:
                return render(request, 'api/login.html', {'error': 'Invalid credentials'})
        except User.DoesNotExist:
            return render(request, 'api/login.html', {'error': 'Invalid credentials'})
    return render(request, 'api/login.html')


def signup(request):
    if request.method == 'POST':
        email = request.POST['signup-email']
        password = request.POST['signup-password']
        user = User(email=email, password=password)
        user.save()
        return render(request, 'api/login.html')
    return render(request, 'api/login.html')


@api_view(['POST'])
def add_task(request):
    print(request.data)
    try:
        serializer = TaskSerializer(data=request.data, partial=True)
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
        user_id = request.GET.get('user_id')
        if user_id:
            tasks = Todo.objects.filter(user=user_id)
        else:
            return Response({"message": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        tasks_serializer = AllTaskSerializer(
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
        serializer = OneTaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
