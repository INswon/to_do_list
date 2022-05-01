from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import User, Task


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse('register and login form')


def todo_list(request: HttpRequest) -> HttpResponse:
    user_id = 1
    user = get_object_or_404(User, pk=user_id)
    tasks = Task.objects.filter(user=user)
    return render(request, 'todo_list/todo_list.html', {'tasks': tasks})
