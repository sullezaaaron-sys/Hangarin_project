from django.contrib import admin
from django.urls import path

from hangarin import views

from hangarin.views import (
    HomePageView,
    TaskList,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
)


urlpatterns = [

    path("admin/", admin.site.urls),

    path(
        "",
        HomePageView.as_view(),
        name="home"
    ),

    path(
        "task_list",
        TaskList.as_view(),
        name="task-list"
    ),

    path(
        "task_list/add",
        TaskCreateView.as_view(),
        name="task-add"
    ),

    path(
        "task_list/<pk>",
        TaskUpdateView.as_view(),
        name="task-update"
    ),

    path(
        "task_list/<pk>/delete",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),

]