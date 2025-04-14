from django.shortcuts import render, redirect
from .forms import StudentSignupForm, TaskForm 
from django.contrib.auth.decorators import login_required
from .models import Student, Task
from django.core.mail import send_mail
from django.contrib.admin.views.decorators import staff_member_required  # Only allow staff/admins
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mass_mail
from django.http import HttpResponse
from .models import Student  # assuming your model is named Student

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'core/signup_success.html')
    else:
        form = StudentSignupForm()
    return render(request, 'core/signup.html', {'form': form})

@login_required
def upload_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save()

            # ✅ Get approved students
            approved_students = Student.objects.filter(is_approved=True)
            print("✅ Approved students:", approved_students)

            # ✅ Send notifications
            for student in approved_students:
                # Send email
                send_mail(
                    subject=f"New Task: {task.title}",
                    message=f"{task.content}\nDue: {task.due_date}",
                    from_email='admin@lexalert.com',
                    recipient_list=[student.email],
                    fail_silently=False,
                )

                # "Send" WhatsApp (simulate for now)
                print(f"📲 Sending WhatsApp to {student.whatsapp}: New Task '{task.title}' due on {task.due_date}")

            return render(request, 'core/upload_success.html')
        else:
            print("❌ Form is not valid:", form.errors)
    else:
        form = TaskForm()

    return render(request, 'core/upload_task.html', {'form': form})


def upload_success(request):
    return render(request, 'core/upload_success.html')

@login_required
def task_list(request):
    tasks = Task.objects.all().order_by('due_date')
    return render(request, 'core/task_list.html', {'tasks': tasks})

@staff_member_required
def admin_dashboard(request):
    students = Student.objects.all()
    
    # ✅ Handle urgency filtering
    urgency = request.GET.get('urgency')
    if urgency:
        tasks = Task.objects.filter(urgency=urgency).order_by('-due_date')
    else:
        tasks = Task.objects.all().order_by('-due_date')

    return render(request, 'core/admin_dashboard.html', {
        'students': students,
        'tasks': tasks,
    })

@staff_member_required
def approve_student(request, student_id):
    student = Student.objects.get(id=student_id)
    student.is_approved = not student.is_approved  # Toggle
    student.save()
    return redirect('admin_dashboard')

def dashboard_view(request):
    urgency = request.GET.get('urgency')
    show_overdue = request.GET.get('overdue') == '1'
    show_today = request.GET.get('due_today') == '1'

    now = timezone.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)

    tasks = Task.objects.all()

    if urgency:
        tasks = tasks.filter(urgency=urgency)

    if show_overdue:
        tasks = tasks.filter(due_date__lt=now)

    if show_today:
        tasks = tasks.filter(due_date__gte=start_of_day, due_date__lt=end_of_day)

    context = {
        'tasks': tasks,
        'show_overdue': show_overdue,
        'show_today': show_today,
        'now': now,
    }
    return render(request, 'dashboard.html', context)

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()

            # ✅ Get all approved students
            approved_students = Student.objects.filter(is_approved=True)

            # ✅ Prepare messages
            messages = []
            for student in approved_students:
                subject = f"New Task: {task.title}"
                message = f"A new task has been added:\n\nTitle: {task.title}\nDue Date: {task.due_date}\nUrgency: {task.urgency}\n\nDescription:\n{task.description}"
                from_email = 'noreply@lexalert.com'
                recipient = student.user.email
                messages.append((subject, message, from_email, [recipient]))

            # ✅ Send all emails at once
            send_mass_mail(messages, fail_silently=False)

            return redirect('dashboard')  # Or wherever you go after task is added
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})

def home(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        student_class = request.POST.get('student_class')
        batch_year = request.POST.get('batch_year')

        # Save to DB
        Student.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            student_class=student_class,
            batch_year=batch_year,
            is_approved=False
        )

        # Send confirmation email
        send_mail(
            'LexAlert Subscription Received',
            'Thank you for subscribing! Our admin will contact you within 24 hours for verification.',
            'no-reply@lexalert.com',
            [email],
            fail_silently=True,
        )

        return render(request, 'core/home.html', {'success': True})

    return render(request, 'core/home.html')