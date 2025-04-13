# send_reminders.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Task, Student
from datetime import timedelta

class Command(BaseCommand):
    help = "Send reminder emails to approved students"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        reminder_days = [1, 3, 5, 7]

        # Get tasks due in the future (up to 7 days from now)
        upcoming_tasks = Task.objects.filter(due_date__gte=now, due_date__lte=now + timedelta(days=7))

        for task in upcoming_tasks:
            days_until_due = (task.due_date - now).days
            if days_until_due in reminder_days:
                approved_students = Student.objects.filter(is_approved=True)
                for student in approved_students:
                    self.stdout.write(f"[EMAIL] To: {student.email} | Task: {task.title} due in {days_until_due} day(s)")
