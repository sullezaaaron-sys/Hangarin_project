from django import forms

from .models import Task, SubTask


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task

        fields = [
            "title",
            "description",
            "deadline",
            "status",
            "category",
            "priority",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4
                }
            ),

            "deadline": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local"
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "priority": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
        }


class SubTaskForm(forms.ModelForm):

    class Meta:
        model = SubTask

        fields = [
            "title",
            "status",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
        }