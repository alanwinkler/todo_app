from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import  CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy
from .models import Task

class TaskList(ListView):
    model = Task
    context_object_name = "tasks"

class TaskDetail(DetailView):
    model = Task
    context_object_name = "task"

class TaskCreate(CreateView):
    model = Task
    # fields = [ 'title', 'description']
    fields = '__all__'
    success_url = reverse_lazy('task')

class TaskUpdate(UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('task')

class TaskDelete(DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('task')