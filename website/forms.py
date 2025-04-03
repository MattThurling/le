from django import forms
from .models import TimeLog
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class TimeLogForm(forms.ModelForm):
    class Meta:
        model = TimeLog
        fields = ['date', 'activity', 'duration']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'activity': forms.TextInput(attrs={'placeholder': 'Activity'}),
            'duration': forms.NumberInput(attrs={'min': '1'}),
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password1", "password2"]
