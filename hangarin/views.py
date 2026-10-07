from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q

from .models import (
    Task,
    Category,
    Priority,
    SubTask,
)



class HomePageView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "home.html"
    context_object_name = "recent_tasks"
    login_url = "/accounts/login/"
    redirect_field_name = "next"

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



class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = "task_list.html"
    context_object_name = "tasks"
    paginate_by = 10
    login_url = "/accounts/login/"
    redirect_field_name = "next"

    SORT_OPTIONS = {
        "deadline": "deadline",
        "-deadline": "-deadline",
        "title": "title",
        "status": "status",
        "priority": "priority__name",
        "category": "category__name",
    }

    def get_queryset(self):
        queryset = (
            Task.objects.select_related("category", "priority")
            .prefetch_related("subtask_set")
            .order_by("-created_at")
        )

        params = self.request.GET

 
        search = params.get("q")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(status__icontains=search) |
                Q(category__name__icontains=search) |
                Q(priority__name__icontains=search)
            )

    
        if params.get("category"):
            queryset = queryset.filter(category_id=params["category"])

        if params.get("priority"):
            queryset = queryset.filter(priority_id=params["priority"])

        if params.get("status"):
            queryset = queryset.filter(status=params["status"])

        # ---- sorting (falls back to newest first) ----
        sort = params.get("sort")
        if sort in self.SORT_OPTIONS:
            queryset = queryset.order_by(self.SORT_OPTIONS[sort], "-created_at")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.all().order_by("name")
        context["priorities"] = Priority.objects.all().order_by("name")
        context["statuses"] = Task._meta.get_field("status").choices

        # keeps filters when you change pages
        params = self.request.GET.copy()
        params.pop("page", None)
        context["querystring"] = params.urlencode()

        return context



class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "task_form.html"
    login_url = "/accounts/login/"
    redirect_field_name = "next"

    fields = [
        "title",
        "description",
        "deadline",
        "status",
        "category",
        "priority",
    ]

    success_url = reverse_lazy("task-list")



class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = "task_form.html"
    login_url = "/accounts/login/"
    redirect_field_name = "next"

    fields = [
        "title",
        "description",
        "deadline",
        "status",
        "category",
        "priority",
    ]

    success_url = reverse_lazy("task-list")



class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "task_del.html"
    login_url = "/accounts/login/"
    redirect_field_name = "next"

    success_url = reverse_lazy("task-list")



class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    template_name = "category_list.html"
    context_object_name = "categories"
    paginate_by = 10
    login_url = "/accounts/login/"
    redirect_field_name = "next"

    def get_queryset(self):
        queryset = Category.objects.all().order_by("name")

        search = self.request.GET.get("q")

        if search:
            queryset = queryset.filter(
                name__icontains=search
            )

        return queryset



class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = "category_form.html"
    login_url = "/accounts/login/"
    redirect_field_name = "next"

    fields = [
        "name",
    ]

    success_url = reverse_lazy("category-list")



class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = "category_form.html"
    login_url = "/accounts/login/"
    redirect_field_name = "next"

    fields = [
        "name",
    ]

    success_url = reverse_lazy("category-list")



class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "category_confirm_delete.html"
    login_url = "/accounts/login/"
    redirect_field_name = "next"

    success_url = reverse_lazy("category-list")



class PriorityList(LoginRequiredMixin, ListView):
    model = Priority
    template_name = "priority_list.html"
    context_object_name = "priorities"
    paginate_by = 10
    login_url = "/accounts/login/"
    redirect_field_name = "next"

    def get_queryset(self):
        queryset = Priority.objects.all().order_by("name")

        search = self.request.GET.get("q")

        if search:
            queryset = queryset.filter(
                name__icontains=search
            )

        return queryset



class PriorityCreateView(LoginRequiredMixin, CreateView):
    model = Priority
    template_name = "priority_form.html"
    login_url = "/accounts/login/"
    redirect_field_name = "next"

    fields = [
        "name",
    ]

    success_url = reverse_lazy("priority-list")



class PriorityUpdateView(LoginRequiredMixin, UpdateView):
    model = Priority
    template_name = "priority_form.html"
    login_url = "/accounts/login/"
    redirect_field_name = "next"

    fields = [
        "name",
    ]

    success_url = reverse_lazy("priority-list")



class PriorityDeleteView(LoginRequiredMixin, DeleteView):
    model = Priority
    template_name = "priority_confirm_delete.html"
    login_url = "/accounts/login/"
    redirect_field_name = "next"

    success_url = reverse_lazy("priority-list")



class SubTaskList(LoginRequiredMixin, ListView):
    model = SubTask
    template_name = "subtask_list.html"
    context_object_name = "subtasks"
    paginate_by = 10
    login_url = "/accounts/login/"
    redirect_field_name = "next"

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



class SubTaskCreateView(LoginRequiredMixin, CreateView):
    model = SubTask
    template_name = "subtask_form.html"
    login_url = "/accounts/login/"
    redirect_field_name = "next"

    fields = [
        "parent_task",
        "title",
        "status",
    ]

    success_url = reverse_lazy("subtask-list")



class SubTaskUpdateView(LoginRequiredMixin, UpdateView):
    model = SubTask
    template_name = "subtask_form.html"
    login_url = "/accounts/login/"
    redirect_field_name = "next"

    fields = [
        "parent_task",
        "title",
        "status",
    ]

    success_url = reverse_lazy("subtask-list")



class SubTaskDeleteView(LoginRequiredMixin, DeleteView):
    model = SubTask
    template_name = "subtask_confirm_delete.html"
    login_url = "/accounts/login/"
    redirect_field_name = "next"

    success_url = reverse_lazy("subtask-list")