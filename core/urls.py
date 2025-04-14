from django.urls import path
from . import views
from .views import home

urlpatterns = [
    path('signup/', views.student_signup, name='student_signup'),
    path('upload/', views.upload_task, name='upload_task'),
    path('upload-success/', views.upload_success, name='upload_success'),
    path('tasks/', views.task_list, name='task_list'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('approve-student/<int:student_id>/', views.approve_student, name='approve_student'),
    path('', home, name='home'),
]
