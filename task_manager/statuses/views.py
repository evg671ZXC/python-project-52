from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from ..utils.mixins import ProtectedErrorMixin
from .models import Status


# Create your views here.
class StatusIndexView(ListView):
    model = Status
    context_object_name = "statuses"


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    template_name_suffix = "_create"
    success_url = reverse_lazy('statuses')
    success_message = _("Status created successfully")
    fields = ['name']


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully changed')
    fields = ['name']


class StatusDeleteView(LoginRequiredMixin,
                       ProtectedErrorMixin,
                       SuccessMessageMixin,
                       DeleteView):
    model = Status
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully deleted')
    error_message = _('Cannot delete status because it is in use')
