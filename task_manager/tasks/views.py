from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Task
from  django.contrib.auth.mixins import LoginRequiredMixin

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
    ...

class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    ...

class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin,  DeleteView):
    model = Task
    ...
