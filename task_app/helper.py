# -*- coding: utf-8 -*-
import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from task_app.forms import TaskForm
from task_app.models import Task, Tag


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


def prepare_context(request, tasks):
    all_count = Task.objects.filter(is_deleted=False, user=request.user).order_by('-created_at').count()
    no_tag_count = Task.objects.filter(is_deleted=False, tags=None, user=request.user, is_done=False).count()
    not_done_count = Task.objects.filter(is_deleted=False, is_done=False, user=request.user).order_by(
        '-created_at').count()
    done_count = Task.objects.filter(is_deleted=False, is_done=True, user=request.user,).order_by('-created_at').count()
    tags = Tag.objects.filter(task__is_deleted=False, task__user=request.user, task__is_done=False).distinct()
    tags_count = []
    for tag in tags:
        tag.task_set = tag.task_set.filter(is_done=False)
    date_now = datetime.date.today()
    page = paginate(tasks, request, 10)
    form = TaskForm()
    context = {
        "tasks": page,
        "all_count": all_count,
        "no_tag_count": no_tag_count,
        "not_done_count": not_done_count,
        "done_count": done_count,
        "tags": tags,
        "date_now": date_now,
        "form": form
    }
    return context


# For correct rendering ajax pagination and date
def prepare_context_ajax(request, tasks):
    date_now = datetime.date.today()
    page = paginate(tasks, request, 10)
    form = TaskForm()
    context = {
        "tasks": page,
        "date_now": date_now,
        "form": form
    }
    return context


def get_ajax_tasks(request):
    tasks = None
    sorting_by = None

    active_sort_title = request.GET.get("active_sort_title")
    active_tag_title = request.GET.get("active_tag_title")
    active_status_title = request.GET.get("active_status_title")

    if active_sort_title == u"По добавлению":
        sorting_by = '-created_at'
    else:
        sorting_by = 'deadline'

    if active_status_title == u"Не сделано":
        tasks = Task.objects.not_done(active_tag_title, request.user, sorting_by)
    elif active_status_title == u"Сделано":
        tasks = Task.objects.done(active_tag_title, request.user, sorting_by)
    else:
        tasks = Task.objects.all_tasks(active_tag_title, request.user, sorting_by)

    return tasks


def get_count_status(request):
    active_tag_title = request.GET.get("active_tag_title")
    active_sort_title = request.GET.get("active_sort_title")
    sorting_by = None
    if active_sort_title == u"По добавлению":
        sorting_by = '-created_at'
    else:
        sorting_by = 'deadline'

    all_status_count = Task.objects.all_tasks(active_tag_title, request.user, sorting_by).count()
    not_done_status_count = Task.objects.not_done(active_tag_title, request.user, sorting_by).count()

    result = {
        "all_status_count": all_status_count,
        "not_done_status_count": not_done_status_count,
        "sorting_by": sorting_by
    }
    return result
