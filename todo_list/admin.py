from django.contrib import admin
from .models import User, ToDoList, Task


class ToDoListInline(admin.TabularInline):
    model = ToDoList
    extra = 2

class UserAdmin(admin.ModelAdmin):
    inilines = [ToDoListInline]


class TaskInline(admin.TabularInline):
    model = Task
    extra = 2

class ToDoListAdmin(admin.ModelAdmin):
    inlines = [TaskInline]


admin.site.register(User, UserAdmin)
admin.site.register(ToDoList, ToDoListAdmin)
