# -*- coding: utf-8 -*-
import datetime
from django import forms
from django.contrib.auth.models import User

from task_app.models import Task, Tag, Profile
from taskmanager import settings


class TaskForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100,
                            widget=forms.TextInput(attrs={'class': 'uk-form-new-task-name',
                                                          'placeholder': 'Введите название',
                                                          'name': 'title',
                                                          'required': 'True'}))

    tags = forms.CharField(label='Tags', required=False, max_length=100,
                           widget=forms.TextInput(attrs={'class': 'uk-form-new-task-tag',
                                                         "placeholder": "Введите теги через запятую",
                                                         "name": "tags"}))
    deadline_default = datetime.date.today()
    deadline = forms.DateField(label='Deadline', widget=forms.TextInput(attrs={'class': "uk-form-deadline",
                                                                               'data-uk-datepicker': "{minDate: '1',format:'YYYY-MM-DD'}",
                                                                               'value': "%s" % deadline_default}))

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        tag_list = set(tags.replace(' ', '').split(','))
        not_allowed = "!#$%^&*()[]:;~|<>?/"
        if 'None' in tag_list:
            self.add_error('tags', 'Нельзя использовать None')
        for tag in tag_list:
            for letter in tag:
                if letter in not_allowed:
                    self.add_error('tags', 'Нельзя использовать символы {}'.format(not_allowed))
                    break
        return tags

    def save(self, author):
        task = Task(title=self.cleaned_data['title'],
                    deadline=self.cleaned_data['deadline'],
                    user=author)
        task.save()
        tags = self.cleaned_data['tags']
        if tags == '':
            return task.id
        else:
            for tag in tags.replace(' ', '').split(','):
                if tag == '':  # В случае ввода нескольких запятых
                    continue
                t = Tag.objects.filter(task__is_deleted=False).filter(task__user=author) \
                    .filter(title=tag).first()
                if t is None:
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

    def save(self, new_data):
        u = User.objects.create_user(new_data['username'],
                                     new_data['email'],
                                     new_data['password1'])
        u.is_active = False
        u.save()
        return u


class UserLoginForm(forms.Form):
    username = forms.EmailField(label='Email', max_length=100, widget=forms.EmailInput(
        attrs={'class': 'input pass',
               'required': 'required',
               'placeholder': 'Email address'}))
    password = forms.CharField(label='Password', max_length=50,
                               widget=forms.PasswordInput(attrs={'class': 'input pass',
                                                                 'placeholder': 'Password (more than 5 char)',
                                                                 'pattern': '.{5,}', 'required': 'required'}))
