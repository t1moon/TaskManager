from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import ListView, CreateView

from task_app.models import Task

tasks = []
categories = []

for i in range(15):
    tasks.append({
        "title": 'ML Cup fixes',
        "description": 'blabla'
    })
for i in range(5):
    categories.append({
        "title": 'Personal'
    })


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
    # tasks = Task.objects.new()
    page = paginate(tasks, request, 10)
    return render(request, 'index.html', {"tasks": page, "categories": categories})
