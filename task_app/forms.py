# -*- coding: utf-8 -*-
import datetime
from django import forms
from task_app.models import Task, Tag, Profile
from taskmanager import settings


class TaskForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'uk-form-new-task-name',
                                                                                                        'placeholder':'Введите название',
                                                                                                        "name": "title"}))
    # description = forms.CharField(label='Text', max_length=5000, widget=forms.Textarea(attrs={'class': 'uk-form-new-task-desc',
    #                                                                                    "placeholder": "Описание..",
    #                                                                                    'rows': '10'}))
    tags = forms.CharField(label='Tags', max_length=100, widget=forms.TextInput(attrs={'class': 'uk-form-new-task-tag',
                                                                                       "placeholder": "Введите теги через запятую",
                                                                                       "name": "tags"}))
    deadline_default = datetime.date.today()
    deadline = forms.DateField(label='Deadline', widget=forms.TextInput(attrs={'class':"uk-form-deadline",
                                                                               'data-uk-datepicker': "{minDate: '1',format:'YYYY-MM-DD'}",
                                                                               'value': "%s" % deadline_default}))

    def save(self):
        task = Task(title=self.cleaned_data['title'],
                    # description=self.cleaned_data['description'],
                    deadline=self.cleaned_data['deadline'])
        task.save()
        for tag in self.cleaned_data['tags'].replace(' ', '').split(','):
            t = Tag.objects.all().filter(title=tag).first()
            if not t:
                t = Tag(title=tag)
                t.save()
            task.tags.add(t)
            task.save()
        return task.id


class UserSignupForm(forms.Form):
    username = forms.EmailField(label='Email', max_length=100, widget=forms.EmailInput(
        attrs={'class': 'input pass',
               'required': 'required',
               'placeholder': 'Email address'}))
    password = forms.CharField(label='Password', max_length=50,
                               widget=forms.PasswordInput(attrs={'class': 'input pass',
                                                                   'placeholder': 'Password (more than 5 char)',
                                                                 'pattern': '.{5,}', 'required': 'required'}))
    password_repeat = forms.CharField(label='Repeat password', max_length=50,
                                     widget=forms.PasswordInput(attrs={'class': 'input pass',
                                                                 'placeholder': 'Confirm the password',
                                                                 'pattern': '.{5,}', 'required': 'required'}))

    def clean_password_repeat(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['password_repeat']
        if password1 != password2:
            self.add_error('password', 'Пароли не совпадают')
        else:
            return password1

    def clean_username(self):
        username = self.cleaned_data['username']
        if Profile.objects.filter(username=username).exists():
            self.add_error('username', 'Данный email уже занят')
        else:
            return username


class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control reg',
               'required': 'required'}))
    password = forms.CharField(label='Password', max_length=50,
                               widget=forms.PasswordInput(attrs={'class': 'form-control reg password',
                                                                 'placeholder': 'Password length (minimum 5)',
                                                                 'pattern': '.{5,}', 'required': 'required'}))
    redirect = forms.CharField(widget=forms.HiddenInput, label='')



