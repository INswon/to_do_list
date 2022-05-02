from django.contrib.auth import authenticate, models, login, logout
from django.db import IntegrityError
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import Task


def index(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponseRedirect('login/')

    tasks = Task.objects.filter(user=request.user)
    return render(
        request,
        'todo_list/todo_list.html',
        {'username': request.user.username, 'tasks': tasks}
    )


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return render(request, 'todo_list/login.html')
    elif request.method != 'POST':
        raise Http404('Request method is not GET or POST.')

    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        raise Http404('Username or password is not set.')

    user = authenticate(request, username=username, password=password)

    if user is None:
        return render(request, 'todo_list/login.html', {'error_message': 'Incorrect username or password.'})

    login(request, user)
    return HttpResponseRedirect('../')


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponseRedirect('../login/')


def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return render(request, 'todo_list/register.html')
    elif request.method != 'POST':
        raise Http404('Request method is not GET or POST.')

    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError as e:
        raise Http404(e)

    try:
        user = models.User.objects.create_user(username=username, password=password)
    except IntegrityError as e:
        raise Http404(f'Username {username} is already registered. Please register another username.')

    login(request, user)
    return HttpResponseRedirect('../')


def check_task_request(request: HttpRequest) -> None:
    if request.method != 'POST':
        raise Http404('Request method is not POST.')

    user=request.user
    if not user.is_authenticated:
        raise Http404('User is not authenticated.')


def create_task(request: HttpRequest) -> HttpResponse:
    check_task_request(request=request)

    name = request.POST.get('name')
    if name is None:
        Http404('Task name is not set.')

    task = Task(user=request.user, name=name)
    task.save()
    return HttpResponseRedirect('../../')


def update_task(request: HttpRequest) -> HttpResponse:
    check_task_request(request=request)

    id_ = request.POST.get('id')
    name = request.POST.get('name')
    if id is None or name is None:
        Http404('Task id or name is not set.')

    task = Task.objects.get(pk=id_)
    task.name = name
    task.save()
    return HttpResponseRedirect('../../')


def delete_task(request: HttpRequest) -> HttpResponse:
    check_task_request(request=request)

    id_ = request.POST.get('id')
    if id is None:
        Http404('Task id is not set.')

    task = Task.objects.get(pk=id_)
    task.delete()
    return HttpResponseRedirect('../../')
