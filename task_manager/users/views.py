from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from ..utils.mixins import UserRequiredMixin, ProtectedErrorMixin
from .forms import RegisterForm


User = get_user_model()


# Create your views here.
class UsersIndexView(ListView):
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = self.model.objects.all().exclude(is_superuser=True)
        return context


class UserCreateView(SuccessMessageMixin, FormView):
    form_class = RegisterForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")
    success_message = _('User successfully registered')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UserUpdateView(UserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy("users")
    success_message = _("User successfully changed")


class DeleteUserView(UserRequiredMixin,
                     ProtectedErrorMixin,
                     SuccessMessageMixin,
                     DeleteView):
    model = User
    success_url = reverse_lazy("users")
    success_message = _("User successfully deleted")
    error_message = _('Cannot delete user because it is in use')
