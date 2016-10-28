from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView

from task_app.forms import TaskForm
from task_app.models import Task, Tag

tasks = []
categories = []
tags =[]

# for i in range(15):
#     tasks.append({
#         "title": 'ML Cup fixes',
#         "description": 'blabla'
#     })
# for i in range(5):
#     categories.append({
#         "title": 'Personal'
#     })


def paginate(object_list, request, on_list):
    list = object_list
    paginator = Paginator(list, on_list)  # Show 25 number_page per page
    page_number = request.GET.get('page')
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.page(paginator.num_pages)
    return page


def index(request):
    tasks = Task.objects.new()
    tags = Tag.objects.all()
    page = paginate(tasks, request, 10)
    form = TaskForm()
    return render(request, 'index.html', {"tasks": page, "tags": tags, "form": form})


def tag(request, tag_name):
    tasks = Task.objects.tag(tag_name)
    tags = Tag.objects.all()
    page = paginate(tasks, request, 10)
    return render(request, 'index.html', {"tasks": page, "tags": tags})

    # return render(request, 'tag.html', {"tasks": page, "tag_name": tag_name})


def add_task(request):
    if request.POST:
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    else:
        form = TaskForm()
    return render(request, 'add_task_modal.html', {"form": form})


def show_task(request):
    task_id = None
    if request.method == 'GET':
        task_id = request.GET['task_id']
    if task_id:
        task = Task.objects.get(id=int(task_id))
        if task:
            title = task.title
    return HttpResponse(title)
