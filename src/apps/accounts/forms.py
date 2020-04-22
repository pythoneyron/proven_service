from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _

from apps.accounts.models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторить пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        exclude = ('',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        user.username = self.cleaned_data["email"]
        user.is_active = True
        user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Повторить пароль', widget=forms.PasswordInput, required=False)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        if self.cleaned_data['password2']:
            user.set_password(self.cleaned_data['password2'])
        user.save()
        return user

    class Meta:
        model = User
        exclude = ('',)


class LoginForm(forms.Form):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={
        'class': 'form-control text_input',
    }))

    phone_number = forms.CharField(max_length=12, widget=forms.TextInput(attrs={
        'class': 'form-control text_input',
        'placeholder': '+70000000000',
    }))

    error_messages = {
        'invalid_login': _("Please enter a correct %(email)s and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }

    def get_user(self):
        return self.user_cache

    def clean(self):
        phone_number = self.cleaned_data.get('phone_number')
        password = self.cleaned_data.get('password')

        if phone_number and password:
            self.user_cache = authenticate(
                phone_number=phone_number,
                password=password
            )
            if self.user_cache is None or self.user_cache.is_active is False:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login'
                )
        return self.cleaned_data


class UpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name')

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
