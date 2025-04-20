from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import date

from .models import Student, Attendance
from .forms import FacultyRegisterForm, AttendanceForm

# ======================
# Authentication Views
# ======================

def register_view(request):
    if request.method == 'POST':
        form = FacultyRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hashing
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = FacultyRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# ======================
# Dashboard View
# ======================
def dashboard(request):
    students = Student.objects.all()
    grouped = {
        'First Year': students.filter(year='First Year'),
        'Second Year': students.filter(year='Second Year'),
        'Third Year': students.filter(year='Third Year'),
    }
    return render(request, 'dashboard.html', {'grouped_students': grouped})

# ======================
# Add Student View (with year)
# ======================

from django.shortcuts import render, redirect, get_object_or_404
from .models import Student

def add_student_with_class(request, year):
    if request.method == 'POST':
        name = request.POST.get('name')
        roll_number = request.POST.get('roll_number')

        if name and roll_number:
            Student.objects.create(name=name, roll_number=roll_number, year=year)
            return redirect('dashboard')

    return render(request, 'add_student.html', {'year': year})


# ======================
# Attendance Views
# ======================

def mark_attendance(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.student = student
            attendance.save()
            return redirect('dashboard')
    else:
        form = AttendanceForm()

    return render(request, 'mark_attendance.html', {'form': form, 'student': student})

def student_attendance_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    attendance_records = Attendance.objects.filter(student=student).order_by('-date')
    return render(request, 'student_attendance_detail.html', {
        'student': student,
        'attendance_records': attendance_records
    })

# ======================
# Delete Student View
# ======================

def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('dashboard')

# ======================
# Grouped Attendance List View
# ======================

def attendance_list(request):
    students = Student.objects.all()
    grouped_students = {}

    for student in students:
        year = student.year
        if year not in grouped_students:
            grouped_students[year] = []
        grouped_students[year].append(student)

    return render(request, 'attendance_list.html', {'grouped_students': grouped_students})

# ======================
# Export Attendance to PDF
# ======================
from django.shortcuts import render
from django.http import HttpResponse
from .models import Student, Attendance
from django.template.loader import get_template
import datetime
import io
from xhtml2pdf import pisa

def export_attendance_pdf(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        try:
            student = Student.objects.get(name__iexact=student_name)
        except Student.DoesNotExist:
            return render(request, 'export_pdf.html', {'error': 'Student not found'})

        # Get all attendance records of that student
        attendance_records = Attendance.objects.filter(student=student)

        template_path = 'attendance_pdf_template.html'
        context = {
            'student': student,
            'attendance_records': attendance_records,
            'date': datetime.datetime.now()
        }

        # Render to PDF
        template = get_template(template_path)
        html = template.render(context)
        result = io.BytesIO()
        pdf = pisa.pisaDocument(io.BytesIO(html.encode('UTF-8')), result)

        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{student.name}_attendance.pdf"'
            return response
        else:
            return HttpResponse('PDF generation error')

    return render(request, 'export_pdf.html')
