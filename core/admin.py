from django.contrib import admin
from .models import Student, Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'urgency', 'created_at')
    list_filter = ('urgency', 'due_date')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'whatsapp', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('name', 'email')