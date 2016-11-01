# -*- coding: utf-8 -*-
import datetime
from django import forms
from task_app.models import Task, Tag
from taskmanager import settings


class TaskForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'uk-form-new-task-name',
                                                                                                        'placeholder':'Название..',
                                                                                                        "name": "title"}))
    # description = forms.CharField(label='Text', max_length=5000, widget=forms.Textarea(attrs={'class': 'uk-form-new-task-desc',
    #                                                                                    "placeholder": "Описание..",
    #                                                                                    'rows': '10'}))
    tags = forms.CharField(label='Tags', max_length=100, widget=forms.TextInput(attrs={'class': 'uk-form-new-task-tag',
                                                                                       "placeholder": "Теги..",
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

