from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.messages.views import SuccessMessageMixin
from  django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task


# Create your views here.
class TaskIndexView(ListView):
    model = Task
    ...

class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/task_list.html'


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin,  CreateView):
    model = Task
    success_url = reverse_lazy('tasks')
    success_message = 'Task created successfully'
    fields = ['name', 'description', 'status', 'performer', 'labels']
    ...

class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    ...

class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin,  DeleteView):
    model = Task
    ...
