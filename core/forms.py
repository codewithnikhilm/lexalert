from django import forms
from .models import Student, Task

class StudentSignupForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'whatsapp']

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],  # Matches HTML date input format
    )

    class Meta:
        model = Task
        fields = ['title', 'content', 'due_date']
