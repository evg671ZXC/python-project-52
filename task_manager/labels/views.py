from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Label


# Create your views here.
class LabelIndexView(ListView):
    model = Label
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    template_name_suffix = "_create"
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully created')
    fields = ['name']


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    success_message = _('Label successfully changed')
    success_url = reverse_lazy('labels')
    fields = ['name']


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully deleted')
    error_message = _('Cannot delete label because it is in use')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.label.all().exists():
            messages.error(request, self.error_message)
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)
