from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from hangarin.models import Priority, Category, Task, Note, SubTask


class Command(BaseCommand):
    help = "Create initial Hangarin data"

    def handle(self, *args, **kwargs):
        fake = Faker()

        priorities = list(Priority.objects.all())
        categories = list(Category.objects.all())

        if not priorities:
            self.stdout.write(
                self.style.ERROR(
                    "No Priority records found. Add the required Priority records first."
                )
            )
            return

        if not categories:
            self.stdout.write(
                self.style.ERROR(
                    "No Category records found. Add the required Category records first."
                )
            )
            return

        tasks = []

        for _ in range(10):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(
                    fake.date_time_this_month()
                ),
                status=fake.random_element(
                    elements=[
                        "Pending",
                        "In Progress",
                        "Completed",
                    ]
                ),
                category=fake.random_element(elements=categories),
                priority=fake.random_element(elements=priorities),
            )

            tasks.append(task)

        for task in tasks:
            Note.objects.create(
                task=task,
                content=fake.paragraph(nb_sentences=2),
            )

            for _ in range(2):
                SubTask.objects.create(
                    parent_task=task,
                    title=fake.sentence(nb_words=4),
                    status=fake.random_element(
                        elements=[
                            "Pending",
                            "In Progress",
                            "Completed",
                        ]
                    ),
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Hangarin initial data created successfully."
            )
        )