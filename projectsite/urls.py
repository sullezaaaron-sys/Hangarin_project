from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from hangarin.views import (
    HomePageView,

    TaskList,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,

    CategoryList,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,

    PriorityList,
    PriorityCreateView,
    PriorityUpdateView,
    PriorityDeleteView,

    SubTaskList,
    SubTaskCreateView,
    SubTaskUpdateView,
    SubTaskDeleteView,

    

)


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),
    path("accounts/", include("allauth.urls")),

    # =========================
    # DASHBOARD
    # =========================

    path(
        "",
        HomePageView.as_view(),
        name="home"
    ),

    # =========================
    # TASKS
    # =========================

    path(
        "task_list/",
        TaskList.as_view(),
        name="task-list"
    ),

    path(
        "task_list/add/",
        TaskCreateView.as_view(),
        name="task-add"
    ),

    path(
        "task_list/<int:pk>/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),

    path(
        "task_list/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),

    # =========================
    # CATEGORIES
    # =========================

    path(
        "categories/",
        CategoryList.as_view(),
        name="category-list"
    ),

    path(
        "categories/add/",
        CategoryCreateView.as_view(),
        name="category-add"
    ),

    path(
        "categories/<int:pk>/",
        CategoryUpdateView.as_view(),
        name="category-update"
    ),

    path(
        "categories/<int:pk>/delete/",
        CategoryDeleteView.as_view(),
        name="category-delete"
    ),

    # =========================
    # PRIORITIES
    # =========================

    path(
        "priorities/",
        PriorityList.as_view(),
        name="priority-list"
    ),

    path(
        "priorities/add/",
        PriorityCreateView.as_view(),
        name="priority-add"
    ),

    path(
        "priorities/<int:pk>/",
        PriorityUpdateView.as_view(),
        name="priority-update"
    ),

    path(
        "priorities/<int:pk>/delete/",
        PriorityDeleteView.as_view(),
        name="priority-delete"
    ),

    # =========================
    # SUBTASKS
    # =========================

    path(
        "subtasks/",
        SubTaskList.as_view(),
        name="subtask-list"
    ),

    path(
        "subtasks/add/",
        SubTaskCreateView.as_view(),
        name="subtask-add"
    ),

    path(
        "subtasks/<int:pk>/",
        SubTaskUpdateView.as_view(),
        name="subtask-update"
    ),

    path(
        "subtasks/<int:pk>/delete/",
        SubTaskDeleteView.as_view(),
        name="subtask-delete"
    ),

    # =========================
    # TYPOGRAPHY
    # =========================

    path(
        "typography/",
        TemplateView.as_view(
            template_name="typography.html"
        ),
        name="typography"
    ),

]