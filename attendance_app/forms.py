from django.contrib.auth.models import User
from django import forms




class FacultyRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']


from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['date', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
