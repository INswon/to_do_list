from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.todo_list, name='list'),
    path('login/', views.login_view, name='login'),
]
