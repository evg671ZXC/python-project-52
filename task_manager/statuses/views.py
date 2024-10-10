from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Status
from ..utils.mixins import UserRequiredMixin

# Create your views here.
class StatusIndexView(ListView):
    model = Status
    context_object_name = "statuses"
    template_name = 'statuses/status_list.html'


class StatusCreateView(UserRequiredMixin, CreateView):
    model = Status
    ...

class StatusUpdateView(UserRequiredMixin, UpdateView):
    model = Status
    ...

class StatusDeleteView(UserRequiredMixin, DeleteView):
    model = Status
    ...