from django.urls import reverse_lazy
# from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from ..utils.mixins import UserRequiredMixin
from .forms import RegisterForm


User = get_user_model()

# Create your views here.
class UsersIndexView(ListView):
    model = User
    context_object_name = "users"




    
class UserCreateView(SuccessMessageMixin, FormView):
    form_class = RegisterForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")
    success_message = 'Пользователь был успешно coздан'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UserUpdateView(UserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy("login")
    success_message = 'Пользователь был успешно обновлен'


class DeleteUserView(UserRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_url = reverse_lazy("users")
    success_message = 'Пользователь был успешно удален'
