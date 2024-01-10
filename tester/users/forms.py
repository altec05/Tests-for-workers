from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import User
from django.forms import ModelForm, FileInput, Form
from django import forms


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'patronymic', 'year_of_birth', 'job', 'department']
        labels = {
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'patronymic': 'Отчество',
            'year_of_birth': 'Год рождения',
            'job': 'Должность',
            'department': 'Отдел',
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control input-box form-ensurance-header-control'})


class ChangePassForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password_1 = forms.CharField(widget=forms.PasswordInput())
    new_password_2 = forms.CharField(widget=forms.PasswordInput())


class ResetPassForm(forms.Form):
    username = forms.CharField(max_length=200)
    year_of_birth = forms.CharField(max_length=4, min_length=4)
    new_password = forms.CharField(widget=forms.PasswordInput())


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'patronymic', 'year_of_birth', 'job', 'department',
                  'password1', 'password2']
        labels = {
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'patronymic': 'Отчество',
            'year_of_birth': 'Год рождения',
            'job': 'Должность',
            'department': 'Отдел',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля'

        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.HiddenInput()
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control input-box form-ensurance-header-control'})
