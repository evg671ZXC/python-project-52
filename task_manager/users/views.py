from django.urls import reverse_lazy
# from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic.list import ListView
# from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseForbidden
from .forms import RegisterForm
from .models import User

# Create your views here.
class UsersIndexView(ListView):
    model = User
    context_object_name = "users"

    
class UserCreateView(FormView):
    form_class = RegisterForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# class AuthDeleteOrUpdateView(UpdateView, DeleteView):
#     model = User

#     def dispatch(self, request, *args, **kwargs):
        
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden()
        
#         return super().dispatch(request, *args, **kwargs)
    
#     def get_success_url(self):
#         return reverse_lazy("users")


class UserUpdateView(UpdateView):
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy("users")

    def dispatch(self, request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        
        return super().dispatch(request, *args, **kwargs)


class DeleteUserView(DeleteView):
    model = User
    success_url = reverse_lazy("users")

    def dispatch(self, request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        
        return super().dispatch(request, *args, **kwargs)