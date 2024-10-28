from django.contrib.auth.mixins import AccessMixin
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect


class UserRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('You are not authorized! Please log in.'))
            return redirect('users')

        if self.get_object() != request.user:
            messages.error(
                request,
                messages.error(request, _("You have't permission!"))
            )
            return redirect('users')

        return super().dispatch(request, *args, **kwargs)
