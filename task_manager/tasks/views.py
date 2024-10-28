from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django_filters.views import FilterView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from task_manager.utils.filters import TaskFilter
from .models import Task
from .forms import TaskForm


# Create your views here.
class TaskIndexView(DetailView):
    model = Task
    template_name = 'tasks/task_show.html'
    context_object_name = 'task'


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    context_object_name = 'tasks'
    template_name_suffix = '_list'
    filterset_class = TaskFilter


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    template_name = 'tasks/task_create.html'
    success_message = _('Task successfully created')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully updated')


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully deleted')
    error_message = _('Only the author can delete the task')

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != request.user:
            messages.error(request, self.error_message)
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)
