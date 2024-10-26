from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "username"]
