# STEP 13 — hangarin/views.py

from django.shortcuts import render
from django.views.generic import ListView


class HomePageView(ListView):

    template_name = "home.html"

    def get_queryset(self):
        return []


class TaskListView(ListView):

    template_name = "task_list.html"

    paginate_by = 10

    def get_queryset(self):
        from .models import Task

        return Task.objects.all()


def typography(request):

    return render(
        request,
        "typography.html"
    )