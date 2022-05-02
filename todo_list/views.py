from django.contrib.auth import authenticate, login
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import Task


def index(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponseRedirect('login/')

    tasks = Task.objects.filter(user=request.user)
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
    return index(request=request)


def register_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Unimplemented page')
