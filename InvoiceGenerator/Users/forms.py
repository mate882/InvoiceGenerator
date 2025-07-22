from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm


from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class EmailBasedPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        active_users = User._default_manager.filter(email__iexact=email, is_active=True)
        return (u for u in active_users if u.has_usable_password())
    

class MinimalSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = None
        self.fields['new_password2'].help_text = None

    def clean(self):
        cleaned_data = super().clean()
        if self.errors.get('new_password1') or self.errors.get('new_password2'):
            self.errors.clear()
            self.add_error(None, _('Password is too weak or does not match.'))
        return cleaned_data


