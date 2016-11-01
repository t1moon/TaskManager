"""taskmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import task_app.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', task_app.views.index, name='index'),
    url(r'^add_task$', task_app.views.add_task, name='add_task'),
    url(r'^edit_task$', task_app.views.edit_task, name='edit_task'),
    url(r'^delete_task$', task_app.views.delete_task, name='delete_task'),
    url(r'^edit_task/(?P<t_id>\d+)/$', task_app.views.edit_task, name='edit_task'),
    url(r'^show_task$', task_app.views.show_task, name='show_task'),
    url(r'^tag/(?P<tag_name>[\w\-!@#$%&*;]+)/$', task_app.views.tag, name='tag'),
]
