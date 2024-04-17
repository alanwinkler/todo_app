from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import  CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from .models import Task

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(user=self.request.user)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            tasks = tasks.filter(title__icontains=search_input)

        task_dicts = []
        for task in tasks:
            task_dict = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'complete': task.complete,
                # Add other fields as needed
            }
            task_dicts.append(task_dict)
            context['tasks'] = task_dicts  # Use a descriptive name like 'task_list'
            context['search_input'] = search_input
            print(task_dict)
        return context



    
    # def get_context_data(self, **kwargs): 
    #     context = super().get_context_data(**kwargs)
    #     context['task'] = Task.objects.filter(user=self.request.user)
    #     context['count'] = context['task'].filter(complete=False).count()

    #     search_input = self.request.GET.get('search-area') or ''
    #     tasks = Task.objects.filter(user=self.request.user)

    #     if search_input:
    #         context['task'] = context['task'].filter(title__icontains=search_input)
    #         # print(context['task'])

    #         context['search_input'] = search_input
    #         task_dicts = []
    #         for task in tasks:
    #             task_dict = {
    #             'id': task.id,
    #             'title': task.title,
    #             'description': task.description,
    #             'complete': task.complete
    #             # Add other fields as needed
    #             }
    #         task_dicts.append(task_dict)
    #         print(task_dict)
    #         return task_dict
    #     return context

    

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = [ 'title', 'description', 'complete']
    # fields = '__all__'
    success_url = reverse_lazy('task')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = [ 'title', 'description', 'complete']
    success_url = reverse_lazy('task')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('task')

class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    fields = "__all__"
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('task')

class RegisterPage(FormView):
    template_name = 'todo/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(RegisterPage, self).get(*args, **kwargs)