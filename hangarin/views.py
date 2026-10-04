from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

from .models import (
    Task,
    Category,
    Priority,
    SubTask,
)


# =========================================================
# DASHBOARD
# =========================================================

class HomePageView(ListView):
    model = Task
    template_name = "home.html"
    context_object_name = "recent_tasks"

    def get_queryset(self):
        return Task.objects.select_related(
            "category",
            "priority"
        ).order_by("-created_at")[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total_tasks"] = Task.objects.count()

        context["pending_tasks"] = Task.objects.filter(
            status="Pending"
        ).count()

        context["completed_tasks"] = Task.objects.filter(
            status="Completed"
        ).count()

        context["in_progress_tasks"] = Task.objects.filter(
            status="In Progress"
        ).count()

        context["total_categories"] = Category.objects.count()

        context["total_priorities"] = Priority.objects.count()

        context["total_subtasks"] = SubTask.objects.count()

        context["categories"] = Category.objects.all().order_by("name")

        context["priorities"] = Priority.objects.all().order_by("name")

        context["subtasks"] = SubTask.objects.select_related(
            "parent_task"
        ).order_by("-created_at")[:5]

        return context


# =========================================================
# TASK LIST
# =========================================================

class TaskList(ListView):
    model = Task
    template_name = "task_list.html"
    context_object_name = "tasks"
    paginate_by = 10

    def get_queryset(self):
        queryset = Task.objects.select_related(
            "category",
            "priority"
        ).order_by("-created_at")

        search = self.request.GET.get("q")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(status__icontains=search) |
                Q(category__name__icontains=search) |
                Q(priority__name__icontains=search)
            )

        return queryset


# =========================================================
# ADD TASK
# =========================================================

class TaskCreateView(CreateView):
    model = Task
    template_name = "task_form.html"

    fields = [
        "title",
        "description",
        "deadline",
        "status",
        "category",
        "priority",
    ]

    success_url = reverse_lazy("task-list")


# =========================================================
# UPDATE TASK
# =========================================================

class TaskUpdateView(UpdateView):
    model = Task
    template_name = "task_form.html"

    fields = [
        "title",
        "description",
        "deadline",
        "status",
        "category",
        "priority",
    ]

    success_url = reverse_lazy("task-list")


# =========================================================
# DELETE TASK
# =========================================================

class TaskDeleteView(DeleteView):
    model = Task
    template_name = "task_del.html"

    success_url = reverse_lazy("task-list")


# =========================================================
# CATEGORY LIST
# =========================================================

class CategoryList(ListView):
    model = Category
    template_name = "category_list.html"
    context_object_name = "categories"
    paginate_by = 10

    def get_queryset(self):
        queryset = Category.objects.all().order_by("name")

        search = self.request.GET.get("q")

        if search:
            queryset = queryset.filter(
                name__icontains=search
            )

        return queryset


# =========================================================
# ADD CATEGORY
# =========================================================

class CategoryCreateView(CreateView):
    model = Category
    template_name = "category_form.html"

    fields = [
        "name",
    ]

    success_url = reverse_lazy("category-list")


# =========================================================
# UPDATE CATEGORY
# =========================================================

class CategoryUpdateView(UpdateView):
    model = Category
    template_name = "category_form.html"

    fields = [
        "name",
    ]

    success_url = reverse_lazy("category-list")


# =========================================================
# DELETE CATEGORY
# =========================================================

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "category_confirm_delete.html"

    success_url = reverse_lazy("category-list")


# =========================================================
# PRIORITY LIST
# =========================================================

class PriorityList(ListView):
    model = Priority
    template_name = "priority_list.html"
    context_object_name = "priorities"
    paginate_by = 10

    def get_queryset(self):
        queryset = Priority.objects.all().order_by("name")

        search = self.request.GET.get("q")

        if search:
            queryset = queryset.filter(
                name__icontains=search
            )

        return queryset


# =========================================================
# ADD PRIORITY
# =========================================================

class PriorityCreateView(CreateView):
    model = Priority
    template_name = "priority_form.html"

    fields = [
        "name",
    ]

    success_url = reverse_lazy("priority-list")


# =========================================================
# UPDATE PRIORITY
# =========================================================

class PriorityUpdateView(UpdateView):
    model = Priority
    template_name = "priority_form.html"

    fields = [
        "name",
    ]

    success_url = reverse_lazy("priority-list")


# =========================================================
# DELETE PRIORITY
# =========================================================

class PriorityDeleteView(DeleteView):
    model = Priority
    template_name = "priority_confirm_delete.html"

    success_url = reverse_lazy("priority-list")


# =========================================================
# SUBTASK LIST
# =========================================================

class SubTaskList(ListView):
    model = SubTask
    template_name = "subtask_list.html"
    context_object_name = "subtasks"
    paginate_by = 10

    def get_queryset(self):
        queryset = SubTask.objects.select_related(
            "parent_task"
        ).order_by("-created_at")

        search = self.request.GET.get("q")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(status__icontains=search) |
                Q(parent_task__title__icontains=search)
            )

        return queryset


# =========================================================
# ADD SUBTASK
# =========================================================

class SubTaskCreateView(CreateView):
    model = SubTask
    template_name = "subtask_form.html"

    fields = [
        "parent_task",
        "title",
        "status",
    ]

    success_url = reverse_lazy("subtask-list")


# =========================================================
# UPDATE SUBTASK
# =========================================================

class SubTaskUpdateView(UpdateView):
    model = SubTask
    template_name = "subtask_form.html"

    fields = [
        "parent_task",
        "title",
        "status",
    ]

    success_url = reverse_lazy("subtask-list")


# =========================================================
# DELETE SUBTASK
# =========================================================

class SubTaskDeleteView(DeleteView):
    model = SubTask
    template_name = "subtask_confirm_delete.html"

    success_url = reverse_lazy("subtask-list")