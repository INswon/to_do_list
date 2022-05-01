from django.contrib.auth import authenticate, login
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import User, Task


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse('register and login form')


def todo_list(request: HttpRequest) -> HttpResponse:
    user_id = 1
    user = get_object_or_404(User, pk=user_id)
    tasks = Task.objects.filter(user=user)
    return render(request, 'todo_list/todo_list.html', {'tasks': tasks})


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return render(request, 'todo_list/login.html')
    elif request.method != 'POST':
        raise Http404('Request method is not GET or POST.')

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is None:
        return render(request, 'todo_list/login.html', {'error_message': 'Incorrect username or password.'})

    login(request, user)
    return todo_list(request=request)
