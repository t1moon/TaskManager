from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import ListView, CreateView

from task_app.models import Task


class ListTaskView(ListView):
    model = Task
    template_name = 'task_list.html'


class CreateTaskView(CreateView):
    model = Task
    fields = ['title', 'description']
    template_name = 'edit_task.html'

    def get_success_url(self):
        return reverse('tasks-list')


def index(request):
    return render(request, 'index.html')
