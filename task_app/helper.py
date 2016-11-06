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
    all_count = Task.objects.filter(is_deleted=False).filter(user=request.user).order_by('-created_at').count()
    no_tag_count = Task.objects.filter(is_deleted=False, tags=None).filter(user=request.user).count()
    not_done_count = Task.objects.filter(is_deleted=False).filter(is_done=False).filter(user=request.user).order_by('-created_at').count()
    done_count = Task.objects.filter(is_done=True).filter(user=request.user).order_by('-created_at').count()
    tags = Tag.objects.filter(task__is_deleted=False).filter(task__user=request.user).distinct()
    page = paginate(tasks, request, 10)
    form = TaskForm()
    context = {
        "tasks": page,
        "all_count": all_count,
        "no_tag_count": no_tag_count,
        "not_done_count": not_done_count,
        "done_count": done_count,
        "tags": tags,
        "form": form
    }
    return context

