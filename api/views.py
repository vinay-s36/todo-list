from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def home(request):
    try:
        if request.user.is_authenticated:
            user_id = request.GET.get('user')
            user = User.objects.get(id=user_id) if user_id else None
            user_email = user.email.split('@')[0] if user else None
            return render(request, 'api/todo.html', {'user': user, 'user_email': user_email})
        else:
            return redirect('login')
    except Exception as e:
        return render(request, 'api/error.html', {'error': str(e)})


def loginpage(request):
    return render(request, 'api/login.html')


def user_login(request):
    try:
        if request.method == 'POST':
            email = request.POST['login-email']
            password = request.POST['login-password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                request.session['email'] = email
                request.session.save()
                redirect_url = f'/todo-list?user={user.id}'
                return redirect(redirect_url)
            else:
                return render(request, 'api/login.html', {'error': 'Invalid credentials'})
        return render(request, 'api/login.html')
    except Exception as e:
        return render(request, 'api/error.html', {'error': str(e)})


def logout(request):
    auth_logout(request)
    try:
        del request.session['email']
    except KeyError:
        pass
    return redirect('login')


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('signup-email')
        password = request.POST.get('signup-password')
        if User.objects.filter(username=email).exists():
            return render(request, 'api/signup.html', {'message': 'User already exists'})
        try:
            new_user = User.objects.create_user(
                username=email, email=email, password=password)
        except Exception as e:
            return render(request, 'api/signup.html', {'message': 'Error creating user'})
        return redirect('login')
    return render(request, 'api/signup.html')


@api_view(['POST'])
def add_task(request):
    try:
        if request.user.is_authenticated:
            serializer = TaskSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def delete_task(request, id):
    try:
        if request.user.is_authenticated:
            task = Todo.objects.get(id=id)
            task.delete()
            return Response({"message": "Task deleted successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    except KeyError:
        return Response({"message": "Task ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    except Todo.DoesNotExist:
        return Response({"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def display_tasks(request):
    try:
        if request.user.is_authenticated:
            user_id = request.GET.get('user_id')
            if user_id:
                tasks = Todo.objects.filter(user=user_id).order_by('title')
            else:
                return Response({"message": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            tasks_serializer = AllTaskSerializer(
                tasks, many=True, context={'request': request})
            data = {
                'tasks': tasks_serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def toggle_task(request, id):
    try:
        if request.user.is_authenticated:
            task = Todo.objects.get(id=id)
        else:
            return Response({"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    except Todo.DoesNotExist:
        return Response({"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = OneTaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
