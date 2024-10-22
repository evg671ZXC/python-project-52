from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm


# Create your views here.
class TaskIndexView(DetailView):
    model = Task
    template_name = 'tasks/task_show.html'
    context_object_name = 'task'


class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/task_list.html'


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin,  CreateView):
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    template_name = "tasks/task_form.html"
    success_message = 'Task created successfully'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    success_message = 'Task successfully updated'


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin,  DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')
    success_message = 'Task successfully deleted'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            messages.error(request, 'Only the author can delete the task')
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

