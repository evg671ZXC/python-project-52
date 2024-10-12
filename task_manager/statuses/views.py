from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Status
from  django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class StatusIndexView(ListView):
    model = Status
    context_object_name = "statuses"
    template_name = 'statuses/status_list.html'


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin,  CreateView):
    model = Status
    ...

class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    ...

class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin,  DeleteView):
    model = Status
    ...