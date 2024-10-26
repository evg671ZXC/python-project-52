from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models.deletion import ProtectedError
from .models import Status


# Create your views here.
class StatusIndexView(ListView):
    model = Status
    context_object_name = "statuses"
    template_name = 'statuses/status_list.html'


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses')
    success_message = 'Status created successfully'
    fields = ['name']


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses')
    success_message = 'Status successfully changed'
    fields = ['name']


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    success_url = reverse_lazy('statuses')
    success_message = 'Status successfully deleted'
    error_message = 'Cannot delete label because it is in use'

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.error_message)
            return redirect(self.success_url)
