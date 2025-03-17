from django import forms
from .models import TimeLog

class TimeLogForm(forms.ModelForm):
    class Meta:
        model = TimeLog
        fields = ['date', 'activity', 'duration']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'activity': forms.TextInput(attrs={'placeholder': 'Activity'}),
            'duration': forms.NumberInput(attrs={'min': '1'}),
        }
