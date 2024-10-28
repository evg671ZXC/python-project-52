from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import views as auth, get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _


def index(request):
    return render(request, 'index.html')


class UserLoginView(SuccessMessageMixin, auth.LoginView):
    model = get_user_model()
    template_name = 'users/login.html'
    success_message = _('You are logged in')


class UserLogoutView(auth.LogoutView):
    success_message = _('You logged out')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, self.success_message)
        return super().dispatch(request, *args, **kwargs)
