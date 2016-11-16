# -*- coding: utf-8 -*-
import random
import sha
import datetime
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from task_app.forms import TaskForm, UserSignupForm, UserLoginForm
from task_app.helper import prepare_context, prepare_context_ajax, get_ajax_tasks
from task_app.models import Task, Tag, Profile
import json
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from taskmanager.settings import EMAIL_HOST_USER


@login_required(login_url='login')
def index(request):
    if request.is_ajax() and request.method == 'GET':
        tasks = get_ajax_tasks(request)
        context = prepare_context_ajax(request, tasks)
        html = render_to_string('task_block.html', context)
        tasks_count = tasks.count()
        response = {
            'html_response': html,
            'not_done_status_count': tasks_count
        }
        return HttpResponse(json.dumps(response), content_type='application/json')

    else:
        sorting_by = '-created_at'
        tasks = Task.objects.not_done(u"Все теги", request.user, sorting_by)
        context = prepare_context(request, tasks)
        return render(request, 'index.html', context)


@csrf_exempt
def delete_task(request):
    if request.method == 'POST':
        t_id = request.POST.get('task_id')
        task = Task.objects.get(id=t_id)
        task.is_deleted = True
        task.save()
        tags = task.tags.all()
        tag_list = []
        for tag in tags:
            tag.task_set.remove(task)
            tag_list.append(tag.title)
        is_done = task.is_done
        response = {
            'tag_list': tag_list,
            'is_done': is_done
        }
        return HttpResponse(json.dumps(response), content_type='application/json')


@csrf_exempt
def complete_task(request):
    if request.is_ajax() and request.method == 'POST':
        t_id = request.POST.get('task_id')
        task = Task.objects.get(id=t_id)

        if request.POST.get('is_done') is not None:
            is_done = request.POST.get('is_done')
            if is_done == 'False' or is_done == 'false':
                task.is_done = True
            else:
                task.is_done = False
        task.save()
        response = {
            'STATUS': 'OK',
            'is_done': task.is_done,
        }
        return HttpResponse(json.dumps(response), content_type='application/json')


@csrf_exempt
def edit_task(request):
    if request.is_ajax() and request.method == 'POST':
        t_id = request.POST.get('task_id')
        task = Task.objects.get(id=t_id)
        response = {
            'STATUS': 'OK'
        }
        if request.POST.get('new_title') is not None:
            task.title = request.POST.get('new_title')

        if request.POST.get('new_deadline') is not None:
            task.deadline = request.POST.get('new_deadline')
            task_is_over = task.deadline <= str(datetime.date.today())
            response['task_is_over'] = task_is_over
        task.save()
        return HttpResponse(json.dumps(response), content_type='application/json')


@csrf_exempt
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            author = Profile.objects.get(username=request.user.username)
            form.save(author)
            return redirect('index')
        else:
            enable_modal = True
            sorting_by = '-created_at'
            tasks = Task.objects.not_done(request.user, sorting_by)
            context = prepare_context(request, tasks)
            context['enable_modal'] = enable_modal
            context['form'] = form
            return render(request, 'index.html', context)
    else:
        form = TaskForm()
    return render(request, 'add_task_modal.html', {'form': form})


@csrf_exempt
def signup(request):
    if request.POST:
        form = UserSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_key = sha.new(salt + username).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            print ("key: ")
            print key_expires
            profile = Profile.objects.create_user(username=username, password=password,
                                                  activation_key=activation_key, key_expires=key_expires)
            profile.is_active = False
            profile.save()
            email_subject = 'Account conformation'
            email_body = '''Hello, %s, and thanks for signing up!
            To activate your account, click this link within 48 hours: http://taskdone.space/confirm/%s''' % \
                         (
                             profile.username,
                             profile.activation_key)
            send_mail(email_subject,
                      email_body,
                      EMAIL_HOST_USER,
                      [profile.username],
                      fail_silently=False)
            return render(request, 'signup.html', {"created": True})
        else:
            return render(request, 'signup.html', {"form": form})
    else:
        form = UserSignupForm()
    return render(request, 'signup.html', {"form": form})


def confirm(request, activation_key):
    profile = get_object_or_404(Profile, activation_key=activation_key)
    if profile.key_expires < timezone.localtime(timezone.now()):
        return render(request, 'confirm.html', {'expired': True})
    profile.is_active = True
    profile.save()
    return render(request, 'confirm.html', {'success': True})


@csrf_exempt
def login(request):
    text_error = None
    if request.POST:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                profile = Profile.objects.get(username=username)
            except:
                text_error = 'Пользователь не найден'
                return render(request, 'login.html', {"form": form, "text_error": text_error})
            if (profile.is_active):
                user = authenticate(username=username, password=password)
                if user:
                    auth_login(request, user)
                    return redirect('index')
                else:
                    text_error = 'Неверный логин или пароль'
            else:
                text_error = 'Email не подтвержден'
        else:
            text_error = 'Невалидная форма'
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {"form": form, "text_error": text_error})


@login_required()
def logout(request):
    auth_logout(request)
    return redirect('login')
