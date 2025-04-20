from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_view, name='register'),  # ✅ Make register page default
    path('dashboard/', views.dashboard, name='dashboard'),  # 🔄 Dashboard moved to its own route

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('add-student/<str:year>/', views.add_student_with_class, name='add_student_with_class'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),

    path('attendance/', views.attendance_list, name='attendance_list'),
    path('mark-attendance/<int:student_id>/', views.mark_attendance, name='mark_attendance'),
    path('student-attendance/<int:student_id>/', views.student_attendance_detail, name='student_attendance_detail'),

    path('export-attendance/', views.export_attendance_pdf, name='export_attendance_pdf'),  # ✅ keep only this one
]
