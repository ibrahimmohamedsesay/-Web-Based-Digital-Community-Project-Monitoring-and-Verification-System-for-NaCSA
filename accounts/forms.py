from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm, PasswordResetForm

from core.forms import StyledFormMixin, StyledModelForm
from .models import Role

User = get_user_model()


class LoginForm(StyledFormMixin, forms.Form):
    username = forms.CharField(label="Username or email", widget=forms.TextInput(attrs={"autofocus": True, "autocomplete": "username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}))
    remember_me = forms.BooleanField(required=False)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        data = super().clean()
        ident, pw = data.get("username"), data.get("password")
        if ident and pw:
            username = ident
            if "@" in ident:
                u = User.objects.filter(email__iexact=ident).first()
                if u:
                    username = u.get_username()
            self.user = authenticate(self.request, username=username, password=pw)
            if self.user is None:
                raise forms.ValidationError("invalid")
            if not self.user.is_active:
                raise forms.ValidationError("inactive")
        return data


class StyledPasswordChange(StyledFormMixin, PasswordChangeForm):
    pass


class StyledSetPassword(StyledFormMixin, SetPasswordForm):
    pass


class StyledPasswordReset(StyledFormMixin, PasswordResetForm):
    def get_users(self, email):
        return (u for u in super().get_users(email) if u.is_active)


class ProfileForm(StyledModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone_number", "department"]


class UserForm(StyledModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput(render_value=False),
                               help_text="Leave blank to keep the current password when editing.")
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "role", "department", "phone_number", "is_active", "password"]

    def clean_password(self):
        pw = self.cleaned_data.get("password")
        if not self.instance.pk and not pw:
            raise forms.ValidationError("A password is required for a new user.")
        if pw:
            from django.contrib.auth.password_validation import validate_password
            validate_password(pw, self.instance)
        return pw

    def save(self, commit=True):
        user = super().save(commit=False)
        pw = self.cleaned_data.get("password")
        if pw:
            user.set_password(pw)
        if commit:
            user.save()
        return user
