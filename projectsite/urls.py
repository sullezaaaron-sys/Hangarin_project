# STEP 14 — projectsite/urls.py

from django.contrib import admin
from django.urls import path

from hangarin.views import (
    HomePageView,
    TaskListView,
    typography,
)


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        HomePageView.as_view(),
        name='home'
    ),

    path(
        'tasks/',
        TaskListView.as_view(),
        name='task-list'
    ),

    path(
        'typography/',
        typography,
        name='typography'
    ),

]