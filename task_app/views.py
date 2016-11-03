from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.core.urlresolvers import reverse
from django.http import HttpResponse, QueryDict, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView

from task_app.forms import TaskForm, UserSignupForm, UserLoginForm
from task_app.models import Task, Tag, Profile
import json

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout


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
    user = request.user
    if (not user.is_authenticated()):
        return redirect('login')
    tasks = Task.objects.not_done(request.user)
    tasks_count = Task.objects.all().count()
    tags = Tag.objects.all()
    page = paginate(tasks, request, 10)
    form = TaskForm()
    return render(request, 'index.html', {"tasks": page, "tasks_count": tasks_count, "tags": tags, "form": form})


def done(request):
    tasks = Task.objects.done(request.user)
    tags = Tag.objects.all()
    page = paginate(tasks, request, 10)
    form = TaskForm()
    return render(request, 'index.html', {"tasks": page, "tags": tags, "form": form})


@csrf_exempt
def delete_task(request):
    if request.method == 'POST':
        t_id = request.POST.get('task_id')
        task = Task.objects.get(id=t_id)
        task.is_deleted = True
        task.save()
        response = {
            'STATUS': 'OK',
        }
        return HttpResponse(json.dumps(response), content_type='application/json')


@csrf_exempt
def edit_task(request):
    if request.is_ajax() and request.method == 'POST':
        t_id = request.POST.get('task_id')
        task = Task.objects.get(id=t_id)

        if request.POST.get('new_title') is not None:
            task.title = request.POST.get('new_title')

        if request.POST.get('new_deadline') is not None:
            task.deadline = request.POST.get('new_deadline')

        if request.POST.get('is_done') is not None:
            is_done = request.POST.get('is_done')
            if is_done == 'False' or is_done == 'false':
                task.is_done = True
            else:
                task.is_done = False
        task.save()
        response = {
            'STATUS': 'OK',
            'is_done': task.is_done
        }
        return HttpResponse(json.dumps(response), content_type='application/json')


def tag(request, tag_name):
    tasks = Task.objects.tag(tag_name, request.user)
    tasks_count = Task.objects.all().count()
    tags = Tag.objects.all()
    page = paginate(tasks, request, 10)
    form = TaskForm()
    return render(request, 'index.html', {"tasks": page, "tasks_count": tasks_count, "tags": tags, "form": form})

@csrf_exempt
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            username = request.user.username
            if (username == ''):
                author=Profile.objects.get(username='timur@mail.ru')
            else:
                author=Profile.objects.get(username=request.user.username)
            form.save(author)
            return redirect('index')
    else:
        form = TaskForm()
    return render(request, 'add_task_modal.html', {"form": form})


@csrf_exempt
def signup(request):
    if request.POST:
        form = UserSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            profile = Profile.objects.create_user(username=username, password=password)
            profile.save()
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('/')
        else:
            return render(request, 'signup.html', {"form": form})
    else:
        form = UserSignupForm()
    return render(request, 'signup.html', {"form": form})


@csrf_exempt
def login(request):
    text_error = None
    if request.POST:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect('index')
            else:
                text_error = 'Wrong password or login'
        else:
            text_error = 'Form is not valid'
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {"form": form, "text_error": text_error})


@login_required()
def logout(request):
    auth_logout(request)
    return redirect('login')
