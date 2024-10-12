from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Label
from  django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class LabelIndexView(ListView):
    model=Label
    context_object_name = 'labels'

class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin,  CreateView):
    model=Label


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    success_message = 'Label successfully changed'


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin,  DeleteView):
    model = Label

